# -*- coding: utf-8 -*- 



import re

#處理掉unicode 和 str 在ascii上的問題
import sys 
import os
import psycopg2
import datetime
#import calendar
#import csv
#import math
#from time import mktime as mktime
import cookielib, urllib2,urllib
from lxml import html,etree
import StringIO
import time as tt
from socket import error as SocketError
import errno
from DB_NOW import DB_NOW


reload(sys) 
sys.setdefaultencoding('utf8') 


class READSITE:
	db = None
	EMPTYNEWS = ("","","","","","")


	def __init__(self,db):
		self.db = db


	#建立更新資料庫
	def rebuildTable(self,sql):
		print '執行重建Table'
		os.system('psql -d %s -f %s'%(self.database,sql))



	def getFullNewsList(self,d):
		self.db.startDB()
		# History Page's example
		# http://news.cnyes.com/rollnews/2014-07-01.htm

		url = 'http://news.cnyes.com/Ajax.aspx?Module=GetRollNews'
		value = urllib.urlencode( {'date' : d.strftime("%Y%m%d")})
		#print url
		#print value
		response = urllib2.build_opener().open(url,value)
		the_page = response.read()
		response.close()		
		page = etree.parse(StringIO.StringIO(the_page))
		total =  len(page.xpath('/NewDataSet/Table1'))

		n = 0 
		for link in page.xpath('/NewDataSet/Table1'):
			# Take a break to avoid disconnection by remote news server
			#tt.sleep(0.5)
			n += 1
			#if n<=1236:
			#	continue
			print "\r%s  [%d /%d](%3.0f%%)"%(d.strftime("%Y-%m-%d"),n,total,n/float(total)*100),
			sys.stdout.flush()

  			title_obj = link.xpath('./NEWSTITLE')[0].text
  			if title_obj is None:
  				continue
  			
			title = title_obj.replace(u"'", u"''")
			ll = 'http://news.cnyes.com'+link.xpath('./SNewsSavePath')[0].text
			typ = link.xpath('./ClassCName')[0].text
			time = d.strftime("%Y-%m-%d")+" "+link.xpath('./NewsTime')[0].text
			rerun = True
			while(rerun):
				try:
					result = self.getDetailNews(ll)
					rerun = False
				except SocketError as e:
					if e.errno != errno.ECONNRESET:
						raise # Not error we are looking for
					print "SocketError=>RERUN"
					rerun = True
					tt.sleep(0.5)
				except UnicodeDecodeError as e:  #也許是被刻意丟錯誤字詞					
					print "UnicodeDecodeError=>PASS"
					rerun = False




			
			if result != self.EMPTYNEWS:
				(author,datetime,title2,info,fulltext,source) = result
				self.db.insertNewsDB((ll,typ,title,info,fulltext,author,time,source))
			#break




	#讀入單頁資訊
	def getDetailNews(self,address):			
		try:
			r = urllib2.build_opener().open(address)
		except urllib2.URLError:
			print "URLError=>address: %s"%address
			return self.EMPTYNEWS

		try:
			page = html.fromstring(r.read().decode('utf-8'))				
			r.close()
			#處理頁面錯誤問題
			if len(page.xpath('//*[@id="form1"]//center/h2'))!=0:		
				return self.EMPTYNEWS
			
			#extract title from content
			title = page.xpath('//*[@class="newsContent bg_newsPage_Lblue"]/h1')[0].text
			#extract info from content
			info = page.xpath('//*[@class="newsContent bg_newsPage_Lblue"]/span[@class="info"]')[0].text
			#print info
			
			#extract datetime from info
			year,month,day,hour,mins = re.match(".*(\d{4})-(\d{2})-(\d{2})\W*(\d{2}):(\d{2})", info,re.U).group(1,2,3,4,5)
			datetime = "%s-%s-%s %s:%s"%(year,month,day,hour,mins)
			#print "info: "+ info
		except IndexError:
			print "IndexError"
			return self.EMPTYNEWS


		#extract author from info
		if re.match(u"鉅亨網新聞中心",info,re.U) is not None:
			author = "新聞中心"
		elif re.match(u"鉅亨台北資料中心",info,re.U) is not None:
			author = "台北資料中心"
		elif re.match(u"鉅亨網\W+.+",info,re.U) is not None:
			author = ""
		elif re.match(u".+記者(\w+)\W+.+",info,re.U) is not None:
			author = re.match(u".+記者(\w+)\W+.+",info,re.U).group(1)
		elif re.match(u".+編譯(\w+)\W+.+",info,re.U) is not None:
			author = re.match(u".+網編譯(\w+)\W+.+",info,re.U).group(1)
		elif re.match(u"鉅亨網(\w+)\W+.+",info,re.U) is not None:
			author = re.match(u"鉅亨網(\w+)\W+.+",info,re.U).group(1)
		elif re.match(u"(\w+)\W+.+",info,re.U) is not None:			
			author = re.match(u"(\w+)\W+.+",info,re.U).group(1)
		#print "author:%s "%author

		#extract source from info 
		source = ""
		pattern = re.match(u".+\W+\(來源：(.+)\)\W+.+",info,re.U) 
		if pattern is not None:
			source = pattern.group(1)
		#print "source: "+source
		
		#extract fulltext from content
		article = page.xpath('//*[@id="newsText"]/p')
		fulltext =''
		text = []
		for a in article:
			if a.text is not None:
				text.append(a.text)
		fulltext = "\n".join(text).replace(u"'", u"''")


		return (author,datetime,title,info,fulltext,source)

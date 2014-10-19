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



reload(sys)
sys.setdefaultencoding('utf8')



class SQL:
	conn = None
	cur = None
	def __init__(self):
		f = open(os.path.abspath('../link.info'),'r')
		self.database = f.readline()[:-1]
		self.user = f.readline()[:-1]
		self.password = f.readline()[:-1]
		self.host = f.readline()[:-1]
		self.port =f.readline()[:-1]
		f.close()
		self.startDB()

	#啟用DB
	def startDB(self):
		self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
		self.cur = self.conn.cursor()
		return self

	#結束DB
	def endDB(self):
		self.cur.close()
		self.conn.close()
		return self

	def getVoteID(self):
		sql = 'SELECT election_id,main_type,title from election';
		self.cur.execute(sql)
		return [(record[0],record[1],record[2]) for record in self.cur.fetchall()]





class VOTE2ELECTION:
	election_id = None
	def __init__(self):
		f = open(os.path.abspath('../link.info'),'r')
		self.database = f.readline()[:-1]
		self.user = f.readline()[:-1]
		self.password = f.readline()[:-1]
		self.host = f.readline()[:-1]
		self.port =f.readline()[:-1]
		f.close()
		self.startDB()

	#啟用DB
	def startDB(self):
		self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
		self.cur = self.conn.cursor()

	#結束DB
	def endDB(self):
		self.cur.close()
		self.conn.close()

	#建立更新資料庫
	def rebuildTable(self,sql):
		print '執行重建Table'
		sql = os.path.abspath('../sql/vote2election.sql')
		os.system('psql -d %s -f %s'%(self.database,sql))

	def map(self):
		sql = "SELECT A.election_id,A.year,A.main_type,C.name from election A left join election_attr C on A.election_id = C.election_id"
		self.cur.execute(sql)
		for row in self.cur.fetchall():
			sql = "SELECT vote_id,title from votecash where title like '%%%s%%' and title like '%%%s%%'  and cond_name = "


	def query_cand_from_github(self,parm):
		[self.election_id,position,title] = parm
		if title.find("不分區")>0 or title.find("任務型國大代表")>0:
			return
		url = "https://raw.githubusercontent.com/kiang/db.cec.gov.tw/master/elections/%s.csv"%self.election_id
		print url
		response = urllib2.build_opener().open(url)
		the_page = response.read()
		response.close()
		lines = the_page.split("\n")
		print parm
		for line in lines[1:] :
			cols = line.split(",")

			if len(cols)<len(lines[0].split(",")):
				break

			[area,name,no,gender,birth_year,party,vote_cnt,vote_rate,elect_ind,incumbent_Ind]= cols

			[sec_name,sec_gender,sec_birth_year] = ["","","NULL"]
			if elect_ind == '':
				elect_ind = "false"
			else:
				elect_ind = "true"

			if incumbent_Ind =="是":
				incumbent_Ind = "true"
			else:
				incumbent_Ind = "false"

			if position =="總統":
				[name,sec_name] = cols [1].split("|")
				[gender,sec_gender] = cols [3].split("|")
				[birth_year,sec_birth_year] = cols [4].split("|")

			if gender =="男":
				gender  = "M"
			else:
				gender = "F"

			if sec_gender =="男":
				sec_gender  = "M"
			elif sec_gender =="女":
				sec_gender = "F"
			name=name.replace("\"","")
			vote_rate = vote_rate[:-1]
			c =",".join( ["election_id", "area", "no", "name", "gender", "birth_year", "sec_name", "sec_gender", "sec_birth_year", "party", "vote_cnt", "vote_rate", "elect_ind", "incumbent_Ind"])
			sql = "INSERT INTO election_record (%s ) VALUES ('%s','%s',%s,'%s','%s',%s,'%s','%s',%s,'%s',%s,%s/100,%s,%s)"%(c,self.election_id, area, no, name, gender, birth_year, sec_name, sec_gender, sec_birth_year, party, vote_cnt, vote_rate, elect_ind, incumbent_Ind)
			print sql
			self.cur.execute(sql)
			self.conn.commit()






	def query_cand(self,input):
		self.election_id = input[0]
		typ = "ctks"
		#grab web
		url = 'http://db.cec.gov.tw/histQuery.jsp?voteCode=%s&qryType=%s'%(self.election_id,typ)
		print url
		response = urllib2.build_opener().open(url)
		the_page = response.read()
		response.close()
		print the_page
		page = self.__parse_html(the_page,typ)
		position = input[1]
		if position == "總統":
			self.record_president(page)

	def record_president(self,page):
		pass

	def query(self,election_id,position,title):
		self.election_id = election_id
		typ = "prof"
		#grab web
		url = 'http://db.cec.gov.tw/histQuery.jsp?voteCode=%s&qryType=%s'%(election_id,typ)
		print url
		response = urllib2.build_opener().open(url)
		the_page = response.read()
		response.close()
		page = self.__parse_html(the_page,typ)
		if position=="總統":
			print "GO PRESIDENT"
			self.attr_president(page)
		elif title.find("不分區")>0 or title.find('任務型國大')>0:
			self.attr_other_special(page)
		else:
			self.attr_other(page)

	def __parse_html(self,the_page,typ):
		lines = the_page.split("\n")
		flag = False
		result = ["<html><body>"]
		for line in lines:
			if line.find('<table class="%s"'%typ)>0:
				flag = True

			if flag==True and line.find('<!--')<0:
				result.append(line)

			if line.find('</table>')>0 :
				flag = False
		result.append("</body></html>")
		result = "\n".join(result)
		print result
		return html.fromstring(StringIO.StringIO(result).getvalue().decode("utf-8"))

	def attr_other_special(self,page):
		tds = page.xpath('//table/tr[3]/td')

		cols =",".join( ["election_id", "area", "population", "election_cnt", "candidate_cnt",  "vote_cnt", "vote_valid", "vote_invalid", "elect_pop_rate", "vote_elect_rate"] )
		area = tds[0].xpath("./a")[0].text.encode("utf-8")
		population = tds[1].text
		election_cnt = tds[2].text
		candidate_cnt= tds[3].text

		vote_cnt= tds[4].text
		vote_valid= tds[5].text
		vote_invalid= tds[6].text
		elect_pop_rate= tds[7].text[:-1]
		vote_elect_rate= tds[8].text[:-1]
		print (cols,self.election_id, area, population, election_cnt, candidate_cnt, vote_cnt, vote_valid, vote_invalid, elect_pop_rate, vote_elect_rate)
		sql = "INSERT INTO election_attr(%s) VALUES ('%s','%s',%s,%s,%s,%s,%s,%s,%s/100,%s/100)"%(cols,self.election_id, area, population, election_cnt, candidate_cnt, vote_cnt, vote_valid, vote_invalid, elect_pop_rate, vote_elect_rate)
		print sql
		self.cur.execute(sql)
		self.conn.commit()

	def attr_other(self,page):

		tds = page.xpath('//table/tr[3]/td')

		cols =",".join(["election_id", "area", "population", "election_cnt", "candidate_cnt", "candidate_male", "candidate_female", "winner_cnt", "winner_male", "winner_female", "vote_cnt", "vote_valid", "vote_invalid", "elect_pop_rate", "vote_elect_rate", "cand_win_rate"])


		area = tds[0].xpath("./a")[0].text.encode("utf-8")
		population = tds[1].text
		election_cnt = tds[2].text
		candidate_cnt= tds[3].text
		candidate_male = tds[4].text
		candidate_female = tds[5].text
		winner_male= tds[6].text
		winner_female= tds[7].text
		winner_cnt= tds[8].text
		vote_cnt= tds[9].text
		vote_valid= tds[10].text
		vote_invalid= tds[11].text
		elect_pop_rate= tds[12].text[:-1]
		vote_elect_rate= tds[13].text[:-1]
		cand_win_rate= tds[14].text[:-1]
		sql = "INSERT INTO election_attr(%s) VALUES ('%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s/100,%s/100,%s/100)"%(cols,self.election_id, area, population, election_cnt, candidate_cnt, candidate_male, candidate_female, winner_cnt, winner_male, winner_female, vote_cnt, vote_valid, vote_invalid, elect_pop_rate, vote_elect_rate, cand_win_rate)
		print sql
		self.cur.execute(sql)
		self.conn.commit()


	def attr_president(self,page):

		tds = page.xpath('//table/tr[3]/td')

		cols =",".join( ["election_id", "area", "population", "election_cnt", "candidate_cnt", "winner_cnt",  "vote_cnt", "vote_valid", "vote_invalid", "elect_pop_rate", "vote_elect_rate", "cand_win_rate"] )
		area = tds[0].xpath("./a")[0].text.encode("utf-8")
		population = tds[1].text
		election_cnt = tds[2].text
		candidate_cnt= tds[3].text
		winner_cnt= tds[4].text
		vote_cnt= tds[5].text
		vote_valid= tds[6].text
		vote_invalid= tds[7].text
		elect_pop_rate= tds[8].text[:-1]
		vote_elect_rate= tds[9].text[:-1]
		cand_win_rate= tds[10].text[:-1]
		sql = "INSERT INTO election_attr(%s) VALUES ('%s','%s',%s,%s,%s,%s,%s,%s,%s,%s/100,%s/100,%s/100)"%(cols,self.election_id, area, population, election_cnt, candidate_cnt, winner_cnt, vote_cnt, vote_valid, vote_invalid, elect_pop_rate, vote_elect_rate, cand_win_rate)
		print sql
		self.cur.execute(sql)
		self.conn.commit()




	def end(self):
		self.endDB()

if __name__ == '__main__':
	#1: sql posistion

	e = VOTE2ELECTION()
	e.rebuildTable()
	e.map()
	e.end()

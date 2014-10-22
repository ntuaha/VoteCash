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


class CHECK:
	year = None
	term = None
	potition = None
	# 1: 全國 2:直轄市長 3:縣市長  4:區/市  5. 村里長
	elect_type = None
	county = None
	district = None
	village = None
	def __init__ (self):
		pass

	def reset(self,database):
		print '重現對照Table'
		filepath = os.path.normpath(os.path.dirname(__file__)+"/../sql/mapping_vote2elect.sql")
		os.system('psql -d %s -f %s'%(database,filepath))



	def getInsertSQL(self,param,table):
		'''
		param  {col,format,value}
		'''
		cols =[]
		formats = []
		values = []
		for p in param:
			cols.append(p['col'])
			formats.append(p['format'])
			values.append(p['value'])
		sql = "INSERT INTO %s (%s) VALUES (%s)" % (table,",".join(cols),",".join(formats))
		sql = sql%tuple(values)
		return sql




class VOTE2ELECTION:
	election_id = None
	check = None
	def __init__(self):
		filepath = os.path.normpath(os.path.dirname(__file__)+"/../link.info")
		#print filepath
		f = open(filepath,'r')
		self.database = f.readline()[:-1]
		self.user = f.readline()[:-1]
		self.password = f.readline()[:-1]
		self.host = f.readline()[:-1]
		self.port =f.readline()[:-1]
		f.close()
		self.check = CHECK()
		self.check.reset(self.database)
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
	def rebuildTable(self):
		print '執行重建Table'
		filepath = os.path.normpath(os.path.dirname(__file__)+"/../sql/vote2election.sql")
		os.system('psql -d %s -f %s'%(self.database,filepath))

	def map(self):
		sql = "SELECT A.election_id,A.area,A.name,B.main_type,B.sub_type,B.term FROM election_record AS A LEFT JOIN election AS B ON A.election_id = B.election_id "
		self.cur.execute(sql)

		results = self.cur.fetchall()
		for row in results:
			(election_id ,area,name,main_type,sub_type,term)= row
			year = int(election_id[0:4])
			term_input= int(term)
			param = []
			param.append({'col':'year','format':"%d",'value':year})
			param.append({'col':'term','format':"%d",'value':term_input})
			param.append({'col':'position','format':"'%s'",'value':main_type})

			if main_type =='總統' and sub_type=='選舉':


				term = '%02d'%int(term)
				# 屆數
				sql = "SELECT vote_id,title from votecash where title like '%%%s%%'  and split_part(cand_name,'、',1) = '%s'"%(term,name)
				#print sql
				self.cur.execute(sql)
				r2 = self.cur.fetchall()
				for rr in r2:
					(vote_id,title) = rr
					# Add category
					param.append({'col':'elect_type','format':"'%s'",'value':'0'})
					self.cur.execute(self.check.getInsertSQL(param,'mapping_vote2elect'))


					sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(vote_id,election_id,area,name,main_type,sub_type,term)
					#print "rr: "+sql
					self.cur.execute(sql)
					self.conn.commit()

			elif main_type =='立法委員' and sub_type=='選舉':
				term = '%d'%int(term)
				# 屆數
				sql = "SELECT vote_id,title from votecash where title like '%%%s%%'  and title like '%%%s%%'  and split_part(cand_name,'、',1) = '%s'"%(term,main_type,name)
				#print sql
				self.cur.execute(sql)
				r2 = self.cur.fetchall()
				for rr in r2:


					sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(rr[0],election_id,area,name,main_type,sub_type,term)
#					print "rr: "+sql
					self.cur.execute(sql)
					self.conn.commit()
			elif main_type =='直轄市長' and sub_type=='選舉':

				if (area=='新北市' or area=='高雄市' or area=='臺中市' or area=='臺南市') and term>95:
					term = "%d"%((int(term)-95)/4)
				else:
					term = '%d'%((int(term)-75)/4)


				# 屆數  地區  屆數
				# 算出 1  卻找到 15
				sql = "SELECT vote_id,title from votecash where title like '%%%s%%'  and title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(term,area,name)
				self.cur.execute(sql)
				r2 = self.cur.fetchall()
				for rr in r2:
					(vote_id,title) = rr
					if int(re.match(".+(\d+).+",title,re.U).groups()[0])==int(term):
						sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(rr[0],election_id,area,name,main_type,sub_type,term)
	#					print "rr: "+sql
						self.cur.execute(sql)
						self.conn.commit()

			elif main_type =='縣市長' and	 sub_type=='選舉':
				#print term
				#print area
				if area=='連江縣':
					term = '%d'%((int(term)-78)/4)
				else:
					term = '%d'%((int(term)-34)/4)

				title = area.decode('utf-8')[-1]+"長"
				# 屆數
				sql = "SELECT vote_id,title,substring(title from '\d+') as term from votecash where title like '%%%s%%'  and title like '%%%s%%'  and  title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(term,area,title,name)
#				print sql
				self.cur.execute(sql)
				r2 = self.cur.fetchall()
				for rr in r2:
					(vote_id,title,term_votecach) = rr
					if int(term_votecach) == int(term):
#					print rr
						sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(rr[0],election_id,area,name,main_type,sub_type,term)
						#print "rr: "+sql
						self.cur.execute(sql)
						self.conn.commit()

			elif main_type =='鄉鎮市長' and sub_type=='選舉':
				term2 = term
				term = '%d'%((int(term)-78)/4)
				title = area.decode('utf-8')[-1]+"長"
				# 屆數
				sql = "SELECT vote_id,title,substring(title from '\d+') as term from votecash where title like '%%%s%%'  and title like '%%%s%%'  and  title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(term,area,title,name)
#				print sql
				self.cur.execute(sql)
				r2 = self.cur.fetchall()
				insert_flag=True
				for rr in r2:
					(vote_id,title,term_votecach) = rr
					if int(term_votecach) == int(term):
#					print rr
						sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(rr[0],election_id,area,name,main_type,sub_type,term)
	#					print "rr: "+sql+"\n"
						self.cur.execute(sql)
						self.conn.commit()
						insert_flag =False

				if insert_flag==True:
					term = '%d'%((int(term2)-34)/4)
					sql = "SELECT vote_id,title,substring(title from '\d+') as term from votecash where title like '%%%s%%'  and title like '%%%s%%'  and  title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(term,area,title,name)
#					print sql
					self.cur.execute(sql)
					r2 = self.cur.fetchall()
					for rr in r2:
						(vote_id,title,term_votecach) = rr
						if int(term_votecach) == int(term):
#						print rr
							sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(rr[0],election_id,area,name,main_type,sub_type,term)
	#						print "rr: "+sql+"\n"
							self.cur.execute(sql)
							self.conn.commit()


			elif main_type =='村里長' and sub_type=='選舉':
				#print term
				#print area
				if int(term) ==99:
					term='99'
				else:
					term = '%d'%((int(term)-78)/4)
				title = area.decode('utf-8')[-1]+"長"
				# 屆數
				sql = "SELECT vote_id,title,substring(title from '\d+') as term  from votecash where title like '%%%s%%'  and title like '%%%s%%'  and  title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(term,area,title,name)
#				print sql
				self.cur.execute(sql)
				r2 = self.cur.fetchall()
				for rr in r2:
#					print rr
					(vote_id,title,term_votecach) = rr
					if int(term_votecach) == int(term):
						sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(rr[0],election_id,area,name,main_type,sub_type,term)
	#					print "rr: "+sql+"\n"
						self.cur.execute(sql)
						self.conn.commit()

				if len(r2) == 0:
					term = '%d'%((int(term2)-34)/4)
					sql = "SELECT vote_id,title from votecash where title like '%%%s%%'  and title like '%%%s%%'  and  title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(term,area,title,name)
#					print sql
					self.cur.execute(sql)
					r2 = self.cur.fetchall()
					for rr in r2:
#						print rr
						sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(rr[0],election_id,area,name,main_type,sub_type,term)
#						print "rr: "+sql+"\n"
						self.cur.execute(sql)
						self.conn.commit()

			elif main_type =='直轄市里長' and sub_type=='選舉':
				#print term
				#print area
				term2 = term
				if int(term) ==99:
					term='99'
				else:
					term = '%d'%((int(term)-79)/4)

					#term = '%d'%((int(term)-75)/4)
				title = area.decode('utf-8')[-1]+"長"
				# 屆數
				sql = "SELECT vote_id,title from votecash where title like '%%%s%%'  and title like '%%%s%%'  and  title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(term,area,title,name)
				#print sql
				self.cur.execute(sql)
				r2 = self.cur.fetchall()
				for rr in r2:
					print rr
					sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(rr[0],election_id,area,name,main_type,sub_type,term)
					#print "rr: "+sql+"\n"
					self.cur.execute(sql)
					self.conn.commit()

				if len(r2) == 0:
					term = '%d'%((int(term2)-95)/4)
					sql = "SELECT vote_id,title from votecash where title like '%%%s%%'  and title like '%%%s%%'  and  title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(term,area,title,name)
					#print sql
					self.cur.execute(sql)
					r2 = self.cur.fetchall()
					for rr in r2:
						#print rr
						sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(rr[0],election_id,area,name,main_type,sub_type,term)
						#print "rr: "+sql+"\n"
						self.cur.execute(sql)
						self.conn.commit()

			elif main_type =='直轄市議員' and sub_type=='選舉':
				#print term
				area = area.decode('utf-8')[0:3]
				#print area
				term2 = term
				if (area=='新北市' or area=='高雄市' or area=='臺中市' or area=='臺南市') and term>95:
					term = "%d"%((int(term)-95)/4)
				elif area=="臺北市":
					term = '%d'%((int(term)-45)/4)
				elif area=="高雄市":
					term = '%d'%((int(term)-63)/4)
				elif area=="臺中市":
					term = '%d'%((int(term)-75)/4)




				title = "市議員"
				# 屆數
				# 對照地區，地名，屆數，職務
				sql = "SELECT vote_id,title,substring(title from '\d+') as term  from votecash where title like '%%%s%%'  and title like '%%%s%%'  and  title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(term,area,title,name)
				#print sql
				self.cur.execute(sql)
				r2 = self.cur.fetchall()
				for rr in r2:
					(vote_id,title,term_votecach) = rr
					if int(term_votecach) == int(term):
					#print rr
						sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(rr[0],election_id,area,name,main_type,sub_type,term)
						#print "rr: "+sql+"\n"
						self.cur.execute(sql)
						self.conn.commit()

			elif main_type =='縣市議員' and sub_type=='選舉':
				#print term
				area = area.decode('utf-8')[0:3]
				#print area

				title = area[2]+"議員"
				# 屆數
				#if area=='臺南市':
				#	sql = "SELECT vote_id,title from votecash where  title='%%16%%' and title like '%%%s%%'  and  title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(area,title,name)
				#else:
				#	sql = "SELECT vote_id,title from votecash where  title like '%%%s%%'  and  title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(area,title,name)
				#print sql
				term = '%d'%((int(term)-30)/4)
				sql = "SELECT vote_id,title from votecash where title like '%%%s%%'  and title like '%%%s%%'  and  title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(term,area,title,name)

				self.cur.execute(sql)
				r2 = self.cur.fetchall()
				for rr in r2:
				#	print rr
					sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(rr[0],election_id,area,name,main_type,sub_type,term)
					#print "rr: "+sql+"\n"
					self.cur.execute(sql)
					self.conn.commit()

			elif main_type =='鄉鎮市民代表' and sub_type=='選舉':
				#print term
				area = re.match('(\D+)第\d{2}選舉區',area,re.U).groups()[0]
				#print area

				title = area.decode('utf-8')[-1]+"民代表"
				# 屆數
				sql = "SELECT vote_id,title from votecash where  title like '%%%s%%'  and  title like '%%%s%%' and split_part(cand_name,'、',1) = '%s'"%(area,title,name)
				#print sql
				self.cur.execute(sql)
				r2 = self.cur.fetchall()
				for rr in r2:
					#print rr
					sql = "INSERT INTO vote2election (vote_id, election_id, area, name, main_type, sub_type, term) VALUES (%s,'%s','%s','%s','%s','%s',%s)"%(rr[0],election_id,area,name,main_type,sub_type,term)
					#print "rr: "+sql+"\n"
					self.cur.execute(sql)
					self.conn.commit()




 #國大代表@@
 #鄉鎮市民代表@@
# 臺灣省議員@@

 #縣市議員@@

# 臺灣省長@@








	def end(self):
		self.endDB()

if __name__ == '__main__':
	#1: sql posistion

	e = VOTE2ELECTION()
	e.rebuildTable()
	e.map()
	e.end()

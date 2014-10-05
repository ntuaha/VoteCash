# -*- coding: utf-8 -*- 


import sys 
import os
import re
import psycopg2
reload(sys) 
sys.setdefaultencoding('utf8') 

class LOADING_ELECTION:
	database=""
	user=""
	password=""
	host=""
	port=""
	conn = None
	cur = None
	def __init__(self,filepath):
		f = open(filepath,'r')
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

	def inputData(self,f):
		fp = open(f,"r")
		#remove header
		fp.readline()
		for record in fp.readlines():
			cols = record[:-1].split(",")
			#代號,選舉名稱,選舉日期
			#20120101P1A1,2012-第13任總統(副總統)選舉,2012-01-14
			election_id = cols[0]
			election_dt = cols[2]
			title = cols[1].replace("\"","").replace(" ","").decode("utf-8")
			R = re.match(u"\"?(\d{4})-\D+",title,re.U)
			if R is not None:
				year = int(R.group(1))
			R = re.match(u"\"?\d+-\D*(\d+)\D+",title,re.U)
			if R is not None:
				term = int(R.group(1))
			R = re.match(u".*(總統|立法委員|任務型國大代表|國大代表|直轄市長|直轄市議員|直轄市里長|縣市長|縣市議員|鄉鎮市長|鄉鎮市民代表|村里長|臺灣省長|臺灣省議員|立委).*",title,re.U)
			if R is not None:
				main_type = R.group(1)
			else:
				raise "ERROR"
			R = re.match(u".*(選舉|補選).*",title,re.U)
			if R is not None:
				sub_type = R.group(1)
			sql = "INSERT INTO election (election_id,election_dt,year,term,main_type,sub_type,title) values ('%s','%s',%d,%d,'%s','%s','%s')"%(election_id,election_dt,year,term,main_type,sub_type,title)
			#print sql
			self.cur.execute(sql)
			self.conn.commit()

		
		fp.close()


	#結束DB
	def endDB(self):	
		self.cur.close()
		self.conn.close()


if __name__ == '__main__':
	#
	os.system(sys.argv[3])
	#link info
	#source data
	LOADING_ELECTION(sys.argv[1]).inputData(sys.argv[2])


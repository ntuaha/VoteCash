# -*- coding: utf-8 -*- 


import sys 
import os
import re
import psycopg2
reload(sys) 
sys.setdefaultencoding('utf8') 

class Loading:
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
		fp.readline()
		for record in fp.readlines():
			cols = record[:-1].split(",")
			#value = ",".join(["'"+x+"'" for x in cols[:-3]])
			value = "'"+cols[0]+"','"+cols[1]+"',"+",".join([x for x in cols[2:-3]])
			r = ["r"+str(i) for i in range(1,7)]
			p = ["p"+str(i) for i in range(1,11)]
			column = ",".join(["title","cand_name"]+r+p)
			sql = "INSERT INTO votecash (%s) values (%s)"%(column,value)
			#print sql
			self.cur.execute(sql)
			self.conn.commit()
			sql = "SELECT max(vote_id) FROM votecash;"
			self.cur.execute(sql)
			data_num  = self.cur.fetchall()[0][0]

			total_r = 0
			for x in map(int,cols[2:8]):
				total_r = total_r +x
			total_p = 0
			for x in map(int,cols[8:18]):
				total_p = total_p +x
			
			rep = cols[0].replace("七","7").replace("二","2")
			R = re.match(u"\D*(\d+)\D*",rep.decode("utf-8"),re.U)
			num = int(R.group(1))
			
			R = re.match(u"(.*)(\d+年?|第\d+任|第\d+屆)(鎮長出缺補選|縣長出缺補選)",rep.decode("utf-8"),re.U)
			if R is not None:
				cols[-3] = R.group(2)
				cols[-1] = R.group(3)
				cols[-2] = R.group(1)

			sql = "INSERT INTO abt01 (vote_id,term,position,area,term_n,total_r,total_p) values (%d,'%s','%s','%s',%d,%d,%d)"%(data_num,cols[-3],cols[-1],cols[-2],num,total_r,total_p)
			#print sql
			self.cur.execute(sql)
			self.conn.commit()
		
		fp.close()


	#結束DB
	def endDB(self):	
		self.cur.close()
		self.conn.close()


if __name__ == '__main__':
	os.system(sys.argv[3])
	Loading(sys.argv[1]).inputData(sys.argv[2])


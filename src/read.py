# -*- coding: utf-8 -*- 

import sys 
import os
import re
reload(sys) 
sys.setdefaultencoding('utf8') 

class PARSER:
	header = None
	data = []
	def __init__(self,f):
		f = open(f,'r')
		self.header = f.readline()[:-1].split(",")
		self.header.append("Time")
		self.header.append("Area")
		self.header.append("Position")
		for line in f.readlines():
			record = line[:-1].split(",")
			record[2:] = map(self.convert,record[2:])	
			print record[0]
			record.extend(self.getTerm(record[0]))
			self.data.append(record)
		f.close()

	def convert(self,string):
		try:
			return int(string)
		except Exception, e:
			return 0

	def getTerm(self,words):
		#re.match(u"\"*非金錢收入總額\D*([\d,]+)\D+",words,re.U)
		R = re.match(u"(\d+年?|第\d+任|第\d+屆)(.*)(鎮長出缺補選|立法委員補選|縣長|縣議員|里長|鄉長|鎮長|市長補選|立法委員補選|鎮長出缺補選|縣長出缺補選|市長|立法委員|鄉長補選|鎮民代表|總統、副總統|市民代表|里長|市議員|鄉民代表|村長|鄉鎮市民代表)",words.decode("utf-8"),re.U)
		if R is not None:
			return R.groups()
		else:
			return ['','','']



	def printRecord(self,record):
		print ",".join(map(str,record))		

	def show(self,num):
		self.printRecord(self.header)
		for i in range(num):
			self.printRecord(self.data[i])
			#self.getTerm(self.data[i][0])
			print ",".join(self.getTerm(self.data[i][0]))

	def output(self,fpath):
		f = open(fpath,'w+')
		f.write(",".join(self.header)+"\n")
		for record in self.data:
			f.write(",".join(map(str,record))+"\n")
		f.close()


if __name__ == '__main__':
	PARSER(sys.argv[1]).output(sys.argv[2])
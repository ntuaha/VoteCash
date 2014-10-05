# -*- coding: utf-8 -*- 

import sys 
import os
import re
reload(sys) 
sys.setdefaultencoding('utf8') 

class Record:
	"""
r01	個人捐贈收入 0  
r02 營利事業捐贈收入 0  
r03 政黨捐贈收入 0  
r04 收 人民團體捐贈收入 0  
r05 入 匿名捐贈收入 0  
r06 其他收入 0 
r062 超過三萬元之收入合計〆0 
r07 金錢收入總額〆0 
r08 收入合計 0 
r09 非金錢收入總額〆0 
p01 人事費用支出 0  
p02 宣傳支出 0  
p03 租用宣傳車輛支出 0  
p04 租用競選辦事處支出 0  
p05 集會支出 0  
p06 出 交通旅運支出 支0  
p07 雜支支出 0  
p08 返還捐贈支出 0  
p09 繳庫支出 0 
p10 專戶存款結存金額〆0 
p102 公共關係費用支出 0  
p11 支出合計 0 
p112 超過三萬元之支出合計〆0 
t1 餘 收支結存金額 0  
t2 絀 金錢以外之賸餘財產 0  
	"""
	area = None
	name = None
	title = None
	r01 = None
	r02 = None
	r03 = None
	r04 = None
	r05 = None
	r06 = None
	r062 = None
	r07 = None
	r08 = None
	r09 = None
	p01 = None
	p02 = None
	p03 = None
	p04 = None
	p05 = None
	p06 = None
	p07 = None
	p08 = None
	p09 = None
	p092 = None
	p10 = None
	p11 = None
	p112 = None
	t1 = None
	t2 = None
	d1 = None
	d2 = None
	d3 = None
	def __init__(self):
		pass
	def header(self):
		b = [u"區域",u"候選人",u"職務"]
		r = [u"個人捐贈收入",u"營利事業捐贈收入",u"政黨捐贈收入",u"人民團體捐贈收入",u"匿名捐贈收入",u"其他收入",u"超過三萬元之收入合計",u"金錢收入總額",u"收入合計",u"非金錢收入總額"]
		p = [u"人事費用支出",u"宣傳支出",u"租用宣傳車輛支出",u"租用競選辦事處支出",u"集會支出",u"交通旅運支出",u"雜支支出",u"返還捐贈支出",u"繳庫支出",u"專戶存款結存金額",u"公共關係費用支出",u"支出合計",u"超過三萬元之支出合計"]
		t = [u"收支結存金額",u"金錢以外之賸餘財產"]
		d = [u"結算日期",u"申報日期",u"更正日期"]
		s =  ",".join(map(str,b+r+p+t+d))
		return s

	def output(self):
		return ",".join(map(str,[self.area,self.name,self.title,self.r01,self.r02,self.r03,self.r04,self.r05,self.r06,self.r062,self.r07,self.r08,self.r09,self.p01,self.p02,self.p03,self.p04,self.p05,self.p06,self.p07,self.p08,self.p09,self.p092,self.p10,self.p11,self.p112,self.t1,self.t2,self.d1,self.d2,self.d3]))


class TF:
	infile=None
	outfile=None
	data = None
	def __init__(self,infile,outfile):
		self.infile = infile
		self.outfile = outfile

	def run(self):

		inF = open(self.infile,'r')
		cand_no = 0
		swift_index = 0
		record = None
		self.data=[]
		for line in inF.readlines():
			swift_index = swift_index+1
			line  = line.decode("utf-8").replace(u"\"","")

			if re.match(u".+99 年直轄市市長選舉擬參選人",line,re.U) is not None or re.match(u"99 年直轄市市長選舉擬參選人",line,re.U) is not None:
				if record is not None:
					self.data.append(record)
				record = Record()
				swift_index = 0
				print "New Record"
				continue

			if swift_index ==1 :
				record.area  = line[:-1]
				continue
				#print str(swift_index)+":"+line
			if swift_index ==2 :
				record.name  = line[:-1]
				continue
				#print str(swift_index)+":"+line

			r01s = re.match(u".*個人捐贈收入\W+([\d,]+)\W+",line,re.U)
			if r01s is not None:				
				record.r01 = float(r01s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.r01)
				continue

			r02s = re.match(u"營利事業捐贈收入\D+([\d,]+)\D+",line,re.U)
			if r02s is not None:
				record.r02 = float(r02s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.r02)
				continue

			r03s = re.match(u"政黨捐贈收入\D+([\d,]+)\D+",line,re.U)
			if r03s is not None:				
				record.r03 = float(r03s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.r03)
				continue


			r04s = re.match(u".*人民團體捐贈收入\D+([\d,]+)\D+",line,re.U)
			if r04s is not None:
				record.r04 = float(r04s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.r04)
				continue

			r05s = re.match(u".*匿名捐贈收入\D+([\d,]+)\D+",line,re.U)
			if r05s is not None:
				record.r05 = float(r05s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.r05)
				continue

			r06s = re.match(u"其他收入\D+([\d,]+)\D+超過三萬元之收入合計〆([\d,]+)\D+",line,re.U)
			if r06s is not None:				
				record.r06 = float(r06s.group(1).replace(",",""))
				record.r062 = float(r06s.group(2).replace(",",""))
				self.debug_print(swift_index,line,record.r06)
				self.debug_print(swift_index,line,record.r062)
				continue


			r07s = re.match(u".*金錢收入總額〆([\d,]+)\D+",line,re.U)
			if r07s is not None:
				record.r07 = float(r07s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.r07)
				continue

			r08s = re.match(u".*收入合計\D+([\d,]+)\D+",line,re.U)
			if r08s is not None:
				record.r08 = float(r08s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.r08)
				continue

			r09s = re.match(u".*非金錢收入總額〆([\d,]+)\D+",line,re.U)
			if r09s is not None:
				record.r09 = float(r09s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.r09)
				continue

			p01s = re.match(u"人事費用支出\D+([\d,]+)\D+",line,re.U)
			if p01s is not None:
				record.p01 = float(p01s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.p01)
				continue

		

			p02s = re.match(u".*宣傳支出\D+([\d,]+)\D+",line,re.U)
			if p02s is not None:
				record.p02 = float(p02s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.p02)
				continue

			p03s = re.match(u"租用宣傳車輛支出\D+([\d,]+)\D+",line,re.U)
			if p03s is not None:
				record.p03 = float(p03s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.p03)
				continue

			p04s = re.match(u"租用競選辦事處支出\D+([\d,]+)\D+",line,re.U)
			if p04s is not None:
				record.p04 = float(p04s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.p04)
				continue
			p05s = re.match(u".*集會支出\D+([\d,]+)\D+",line,re.U)
			if p05s is not None:
				record.p05 = float(p05s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.p05)
				continue

			p06s = re.match(u".*交通旅運支出\D+([\d,]+)\D+",line,re.U)
			if p06s is not None:
				record.p06 = float(p06s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.p06)
				continue

			p07s = re.match(u".*雜支支出\D+([\d,]+)\D+",line,re.U)
			if p07s is not None:
				record.p07 = float(p07s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.p07)
				continue

			p08s = re.match(u"返還捐贈支出\D+([\d,]+)\D+",line,re.U)
			if p08s is not None:
				record.p08 = float(p08s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.p08)
				continue

			p09s = re.match(u".*繳庫支出\D+([\d,]+)\D+專戶存款結存金額〆([\d,]+)\D+",line,re.U)
			if p09s is not None:
				record.p09 = float(p09s.group(1).replace(",",""))
				record.p092 = float(p09s.group(2).replace(",",""))
				self.debug_print(swift_index,line,record.p09)
				self.debug_print(swift_index,line,record.p092)
				continue

			p10s = re.match(u"公共關係費用支出\D+([\d,]+)\D+",line,re.U)
			if p10s is not None:
				record.p10 = float(p10s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.p10)
				continue

			p11s = re.match(u".*支出合計\D+([\d,]+)\D+超過三萬元之支出合計〆([\d,]+)\D+",line,re.U)
			if p11s is not None:
				record.p11 = float(p11s.group(1).replace(",",""))
				record.p112 = float(p11s.group(2).replace(",",""))
				self.debug_print(swift_index,line,record.p11)
				self.debug_print(swift_index,line,record.p112)
				continue

			t1s = re.match(u".*收支結存金額 ([\d\-,]+)\D+",line,re.U)
			if t1s is not None:
				record.t1 = float(t1s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.t1)
				continue

			t2s = re.match(u".*金錢以外之賸餘財產 ([\d\-,]+)\D+",line,re.U)
			if t2s is not None:
				record.t2 = float(t2s.group(1).replace(",",""))
				self.debug_print(swift_index,line,record.t2)
				continue

			d1s = re.match(u"結算日期〆([\d]+)\D+([\d]+)\D+([\d]+)\D+",line,re.U)
			if d1s is not None:
				year = float(d1s.group(1).replace(",",""))+1911
				month = float(d1s.group(2).replace(",",""))
				day = float(d1s.group(3).replace(",",""))
				record.d1 = "%04d%02d%02d"%(year,month,day)
				self.debug_print(swift_index,line,record.d1)
				continue

			d2s = re.match(u"申報日期〆([\d]+)\D+([\d]+)\D+([\d]+)\D+",line,re.U)
			if d2s is not None:
				year = float(d2s.group(1).replace(",",""))+1911
				month = float(d2s.group(2).replace(",",""))
				day = float(d2s.group(3).replace(",",""))
				record.d2 = "%04d%02d%02d"%(year,month,day)
				self.debug_print(swift_index,line,record.d2)
				continue

			d3s = re.match(u"更正日期〆([\d]+)\D+([\d]+)\D+([\d]+)\D+",line,re.U)
			if d3s is not None:
				year = float(d3s.group(1).replace(",",""))+1911
				month = float(d3s.group(2).replace(",",""))
				day = float(d3s.group(3).replace(",",""))
				record.d3 = "%04d%02d%02d"%(year,month,day)
				self.debug_print(swift_index,line,record.d2)
				continue




			#if swift_index>10 :
			#	break
		self.data.append(record)
		inF.close()
		self.output()
	

	def debug_print(self,index,line,check):
		print str(index)+":"+line[:-1]
		print check

	def output(self):
		outF = open(self.outfile,'w+')
		basicRecord = Record()
		outF.write(basicRecord.header()+"\n")
		for r in self.data:
			outF.write(r.output()+"\n")
		outF.close()






if __name__ == "__main__":
	TF(sys.argv[1],sys.argv[2]).run()

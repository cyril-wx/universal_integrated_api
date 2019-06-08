#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
常用工具类
"""
import sys
import os
import csv


def readCMD(args=[], isShell=True):
	'''
    #Running the command and read String from stdout. (Support py2/py3)
    #@param args(list): cmd script path & cmd params
    #@param isShell(Bool): The cmd is shell cmd or not.
    #@param timeout(int): set timeout(must > 0), default -1 means never timeout
    #@return (res, rev): res: result status code
    #                   rev: result string
    '''
	import subprocess
	from subprocess import Popen

	res = False
	rev = []
	p = subprocess.Popen(args, shell=isShell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	while True:
		if sys.version > "3":  ## python3 +
			buff = p.stdout.readline().decode(encoding="UTF-8").strip().replace("\r\n", "")
		else:                   ## python2 +
			buff = p.stdout.readline().strip().replace("\r\n", "")

		if p.poll() != None:
			if buff == '':
				break;
		if buff != '':
			buff.strip().replace("\n", "")
			rev.append(buff)
			# print(buff)
#    if p.wait() == 0:
#        res = True

	return (p.wait(), rev)  ## res(Bool): The cmd is running successful?
							## rev(String): The cmd result string.
def getLocalHostIP():
	"""
	# 获取本机 IP, 暂不支持存在多IP环境的本机IP获取。
	:return: IP(str)
	"""
	cmd = "/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d \"addr:\" | sed -n 1p"
	IP = None
	try:
		IP = readCMD([cmd], True)[1][0]
	except Exception as e:
		print(e)
	finally:
		return IP

def fileDataCompare(f_1, f_2):
	"""
	# 文件内容对比(仅限文本文档)
	:param f_1:
	:param f_2:
	:return:  True/False
	"""
	a = None
	b = None
	try:
		f_a = open(f_1, "r")
		f_b = open(f_2, "r")

		while True:
			a = f_a.readline()
			b = f_b.readline()
			if not a and not b:
				break
#			elif a.strip() == "" or b.strip() == "":       # 这里的作用就是检测文末是否存在空行，但影响执行效率
#				continue
			elif a != b:
				return False

	except Exception as e:
		print("Can't open file_1-%s or file_2-%s" %(f_1, f_2))
		print(e)
		return False
	finally:
		if f_a:
			f_a.close()
		if f_b:
			f_b.close()
		return True

# --csv 文件读写操作2 --
# Create on 18/12/05 by Cyril
def print2DList(_2DList):
	"""
	打印二维列表
	:param _2DList:
	:return: None
	"""
	if _2DList:
		try:
			for line in _2DList:
				print(line)
		except Exception as e:
			print("print2DList -> Error _2DList data type.")
			print(e)
		finally:
			print("print2DList -> Finish.")

def readCSVFile(filePath):
	"""
	# 读取csv文件 (obj.dict)
	:param filePath:
	:return: [] / None
	"""
	mdata = []
	if(os.path.exists(filePath)):
		if sys.version > "3":      # 兼容py3版本
			with open(filePath, 'r', newline='', encoding="UTF-8-sig") as f:
				lines = csv.reader(f, dialect='excel')
				for line in lines:
					mdata.append(line)
			print2DList(mdata)
			print ("readCSVFile -> Reading successful.")
		else:                       # 兼容py2版本
			with open(filePath, 'r') as f:
				lines = csv.reader(f, dialect='excel')
				for line in lines:
					mdata.append(line)
			print2DList(mdata)
			print ("readCSVFile -> Reading successful.")
	else:
		print('readCSVFile -> no file: %s' %filePath)
		mdata = None
	return mdata

def writeCSVFile(filePath, _2DList):
	"""
	# 写入csv文件（obj.dict）
	# 若csv文件存在，则追加写入
	:param filePath:
	:param _2DList:
	:return: True/False
	"""
	if(os.path.exists(filePath)):
		if sys.version > "3.5":     # 兼容py3版本
			csvfile = open(filePath, 'a', newline='', encoding="UTF-8") # newline='' 为python3
		else:                       # 兼容py2版本
			csvfile = open(filePath, 'a')

		writer_ = csv.writer(csvfile, dialect='excel')
		if isinstance(_2DList, (list)):
			try:
				for line in _2DList:
					writer_.writerow(line)
				print ("writeCSVFile -> Writing successful.")
				return True
			except Exception as e:
				print ("writeCSVFile -> Error data type")
				print("TEST -> ",e)
				return False
		else:
			print ("writeCSVFile -> Error data type")
	else:
		dirname, filename = os.path.split(os.path.abspath(filePath))
		if(os.access(dirname, os.W_OK)):  #检查路径是否可写，即是否可创建文件
			cmd = 'cd '+ dirname + ' ; touch ' + filename + ' ;'
			os.system(cmd)
			writeCSVFile(filePath, _2DList)
			return True
		else:
			print("writeCSVFile -> Current path no access to create files.")
	return False

if "__main__" == __name__:
	dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
	#filePath = dirname+"/csvData.csv"
	filePath = '/tmp/autopanic_ips_stats.csv'
	print("filePath : ", filePath)

	data=[]
	data.append(['s1', 'Online', 'master'])
	data.append(['s2', 'Online', 'slave'])
	data.append(['s3', 'Online', 'slave'])
	data.append(['s4', 'Online', 'slave'])
	data.append(['s5', 'Online', 'slave'])
	#writeCSVFile(filePath, _2DList=data)
	readCSVFile(filePath)


#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
#**********************************************	#
# 常用工具类（模块）                               #
#----------------------------------------------	#
# @Author: Cyril				                #
# @Mail: 848873227@qq.com                       #
# @Create: 2019-06-08				            #
# @Tips:                                        #
#**********************************************	#
"""
import sys
import os
import logging


def readCMD(args=[], isShell=True):
	'''
    #Running the command and read String from stdout. (Support py2/py3)
    #@param args(list): cmd script path & cmd params
    #@param isShell(Bool): The cmd is shell cmd or not.
    #@param timeout(int): set timeout(must > 0), default -1 means never timeout
    #@return (res, rev): res: stdout status code(int)
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

def pingRemoteIP():
	pass

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

def my_logger(log_obj):
	"""
	# 自定义log显示及输出
	:param log_obj: object name who exec logger
	:return: logger obj
	"""
	logger = logging.getLogger(log_obj)
	#print(logger.handlers)
	logger.setLevel(logging.INFO)

	console_handle = logging.StreamHandler()
	file_handle = logging.FileHandler(filename=log_obj+".log")
	formatter = logging.Formatter('%(asctime)s - %(name)s:%(funcName)s - %(levelname)s - %(message)s ')
	console_handle.setFormatter(formatter)
	file_handle.setFormatter(formatter)
	logger.addHandler(console_handle)
	logger.addHandler(file_handle)

	return logger


if "__main__" == __name__:
	dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

	## 初始化一个log管理器
	mlog=my_logger("jc_utils")

	#filePath = dirname+"/csvData.csv"
	filePath = '/tmp/autopanic_ips_stats.csv'
	mlog.info("filePath : ", filePath)

	data=[]
	data.append(['s1', 'Online', 'master'])
	data.append(['s2', 'Online', 'slave'])
	data.append(['s3', 'Online', 'slave'])
	data.append(['s4', 'Online', 'slave'])
	data.append(['s5', 'Online', 'slave'])
	#writeCSVFile(filePath, _2DList=data)
	from csv_rw import readCSVFile
	readCSVFile(filePath)


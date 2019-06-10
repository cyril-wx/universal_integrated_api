#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
#**********************************************	#
# csv 文件读写操作工具                            #
#----------------------------------------------	#
# @Author: Cyril				                #
# @Mail: 848873227@qq.com                       #
# @Create: 2019-06-08				            #
# @Tips:                                        #
#**********************************************	#
"""
import sys
import os
import csv
from jc import utils as jt

# 使用默认的 Logger 配置
#logging.basicConfig(handlers=[logging.FileHandler("jc_utils.log", encoding="utf-8")], filemode="w", format="[%(asctime)s] %(levelname)s: [%(funcName)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
#logging.basicConfig(filename='jc_utils.log',level=logging.DEBUG,format='%(asctime)s %(filename)s [line:%(lineno)d] %(message)s',datefmt='%Y-%m-%d')

## 初始化一个log处理器
mlog=jt.my_logger("jc_csv_rw")

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
			mlog.warning("print2DList -> Error _2DList data type.")
			mlog.exception(e)
		finally:
			mlog.info("print2DList -> Finish.")


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
			mlog.info("Reading successful.")
			mlog.info(mdata)
		else:                       # 兼容py2版本
			with open(filePath, 'r') as f:
				lines = csv.reader(f, dialect='excel')
				for line in lines:
					mdata.append(line)
			#print2DList(mdata)
			mlog.info ("Reading successful.")
	else:
		mlog.warning('Not found file: %s' %filePath)
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
		if isinstance(_2DList, list):
			try:
				for line in _2DList:
					writer_.writerow(line)
				mlog.info ("Writing successful.")
				return True
			except Exception as e:
				mlog.warning ("Error data type")
				mlog.exception(e)
				return False
		else:
			print ("Error data type")
	else:
		dirname, filename = os.path.split(os.path.abspath(filePath))
		if(os.access(dirname, os.W_OK)):  #检查路径是否可写，即是否可创建文件
			cmd = 'cd '+ dirname + ' ; touch ' + filename + ' ;'
			os.system(cmd)
			writeCSVFile(filePath, _2DList)
			mlog.info("Writing csv file successfully.")
			return True
		else:
			mlog.exception("Current path no access to create files.")
	return False

if __name__ == "__main__":
	writeCSVFile("/tmp/test.csv", [
		[1,2,3,4,5],
		[21, 22, 23, 24, 25],
		[31, 32, 33, 34, 35],
	])

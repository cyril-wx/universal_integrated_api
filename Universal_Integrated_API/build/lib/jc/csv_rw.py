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
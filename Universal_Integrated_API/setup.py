#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
#**********************************************	#
# setup for Universal_Integrated_API            #
# Universal_Integrated_API的构建及安装模块        #
#----------------------------------------------	#
# @Author: Cyril				                #
# @Mail: 848873227@qq.com                       #
# @Create: 2019-06-08				            #
# @Tips:                                        #
#**********************************************	#
"""
from distutils.core import setup
setup(
	name="Universal_Integrated_API", 
	version="1.0.5",
	description="Universal Integrated APIs", 
	author="Cyril",
	author_email="848873227@qq.com",
	py_modules=[
		"jc.utils",
		"jc.csv_rw",
		"jc.rsync_tools",
		"jc.mariadb_helper",
	    "jc.func_test",
	    "jc.SqliteTools",
	    "jc.MyLogger",
	    "jc.IP_Pool",
	    "jc.ExecTimeAnalysis",

	])

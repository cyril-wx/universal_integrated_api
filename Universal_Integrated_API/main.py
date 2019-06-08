#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
#**********************************************	#
# main test for Universal_Integrated_API        #
# 测试                                           #
#----------------------------------------------	#
# @Author: Cyril				                #
# @Mail: 848873227@qq.com                       #
# @Create: 2019-06-08				            #
# @Tips:                                        #
#**********************************************	#
"""
from jc import utils

utils.test()
print utils.readCMD(["ls"], True)

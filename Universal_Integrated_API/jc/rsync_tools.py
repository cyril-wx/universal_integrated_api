#!/usr/bin/python
# -*- coding:UTF-8 -*-
#**********************************************	#
# Master and Slave rsync Tools       			#
# AutoPanic主从服务器同步工具	                    #
#----------------------------------------------	#
# @Author: Cyril								#
# @Mail: 848873227@qq.com                       #
# @Create: 2019-06-08	                        #
# @Modify: 2019-06-10                           #
# @Tips: 			                            #
#**********************************************	#

from jc import utils as jt
from jc import csv_rw as jcsv
import os
import re
import sys


class SyncTool:
	#logger = logging.getLogger("TEST").setLevel(logging.DEBUG)
	# 使用默认的 Logger 配置
	# logging.basicConfig(handlers=[logging.FileHandler("jc_utils.log", encoding="utf-8")], filemode="w", format="[%(asctime)s] %(levelname)s: [%(funcName)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

	ip_pool = []    # 二维数组
	conf_path = "/tmp/autopanic_ips_stats.csv"
	tmp_csv_file = "/tmp/1.csv"
	origin_data=[
		["Station", "IP", "Stats", "role"],
		["s1", "172.21.156.46", "Online", "master"],
		["s2", "172.21.204.237", "Online", "slave"],
		["s3", "172.21.204.238", "Online", "slave"],
		["s4", "172.21.204.239", "Online", "slave"],
	]

	def __init__(self, conf_path=conf_path):
		"""
		# 初始化
		:param conf_path: 配置文件，存放集群内所有机器IP,csv文件格式存储
		"""
		# 初始化一个log处理器
		self.mlog = jt.my_logger("jc_rsync_ptool")
		try:
			self.ip_pool = jcsv.readCSVFile(conf_path)
			self.ip_pool.remove(self.ip_pool[0])
			conf_parent_path = os.path.split(conf_path)[0]
		except Exception as e:
			self.mlog.warning("%s initializing failed." %__name__)
			self.mlog.exception(e)
		else:
			self.mlog.info("%s initializing successd." %__name__)


#	def run_IP_Pool(self):
#		pass

	'''
	def setIPStats(self, IP, Stats="Online"):
		"""
		# Add/Update IPStats to local IP_Pool
		# 请勿直接调用此方法
		:param IP:
		:param Stats: Online/Offline (str)
		:return: True/False
		"""
		print (self.ip_pool)
		'''

	def fullSync(self, remoteIP, syncFileOrDir, reverse=False, remoteUser="gdlocal", remotePWD="gdlocal"):
		"""
		# Full synchronization
		# 两个工站进行全量同步 (旧版本不会覆盖新版本文件)
		:param remoteIP: 远程工站IP需手动指定
		:param syncFileOrDir: 要同步的文件或文件夹
		:param reverse: 是否反向同步 True/False
						# False: 正向同步，直接覆盖远程文件
						# True: 反向同步，即下载远程文件到本地临时文件/tmp/1.csv
		:param remoteUser: 被同步文件工站用户名
		:param remoteUser: 被同步文件工站用户密码
		:return: True/False
		"""
		if not re.match("\d+.\d+.\d+.\d+", remoteIP):
			self.mlog.exception("'IP' is invalid type.")
			exit(1)

		(dir, filename) = os.path.split(syncFileOrDir)
		## -u 同步时旧版本不会覆盖新版本
		if reverse:
			sync_cmd = "/usr/bin/rsync -avu %s@%s://%s %s" %( remoteUser, remoteIP, syncFileOrDir, self.tmp_csv_file)
		else:
			sync_cmd = "/usr/bin/rsync -avu %s %s@%s://%s" % (syncFileOrDir, remoteUser, remoteIP, dir)
		self.mlog.debug("sync_cmd=%s" % sync_cmd)
		cmd = """
	expect << EOF
	set timeout 3
	spawn %s
	expect {
			-re "Are you sure you want to continue connecting (yes/no)?" { send "yes\r"; exp_continue }
	        -re "Password:" { send "%s\r"; exp_continue }
	        -re "total size is" { exit 0}
	    timeout {
	        send_user "Timeout...exit.\r" ;
	        exit 1
	    }
	        eof {
	                send_user "EOF finish.\r" ;
	                exit 2
	        }
	}
	EOF
	        """ %(sync_cmd, remotePWD)

		(res, rev) = jt.readCMD(cmd, True)
		if res == 0:
			self.mlog.info("Get remote file successul. [IP:%s]" % remoteIP)
		else:    ## rsync 有可能失败，尝试重试
			(res, rev) = jt.readCMD(cmd, True)
			if res != 0:
				self.mlog.warning("Get remote file failed. [IP:%s], exiting..." % remoteIP)
				return False
			else:
				self.mlog.info("Retry get remote file successul. [IP:%s]" % remoteIP)
		return True

	def increSync(self, remoteIP, syncFileOrDir, remoteUser="gdlocal", remotePWD="gdlocal"):
		"""
		# Incremental synchronization
		# 两个工站进行增量同步 （其中一个是本机）
		# Tips: 适用于单文件单增量同步，传入单syncFileOrDir若是文件夹则可能失败
		:param remoteIP: 远程工站IP需手动指定
		:param syncFileOrDir: 要同步的文件或文件夹
		:param reverse: 是否反向同步 True/False, 默认正向同步False
		:param remoteUser: 被同步文件工站用户名
		:param remoteUser: 被同步文件工站用户密码
		:return: True/False
		"""
		if not os.path.isfile(syncFileOrDir):
			self.mlog.warning("'%s' should be a exist file path." %syncFileOrDir)
			# return False

		# 反向同步，即下载远程文件到本地. 如果失败则退出。
		if not self.fullSync(remoteIP, syncFileOrDir, True, remoteUser, remotePWD):
			self.mlog.exception("Failed: Can't get remote file from [IP:%s]." %remoteIP )
			return False

		remote_data = jcsv.readCSVFile(self.tmp_csv_file)
		local_data = jcsv.readCSVFile(syncFileOrDir)
		jt.readCMD(["rm -rf %s" %self.tmp_csv_file], True )
		## 将本地数据与远程数据对比合并重复项，并写入新数据
		if remote_data and local_data and remote_data == local_data:
			## 如果数据对比相同则不写入新数据和远程同步
			return True
		else:
			new_data = self.mergeLists(remote_data, local_data)
			# 清空原数据表
			with open(syncFileOrDir, "w") as f:
				f.write("")
			jcsv.writeCSVFile(syncFileOrDir, new_data)
			if self.fullSync(remoteIP, syncFileOrDir, False, remoteUser, remotePWD):
				return True
		return False

	def increSyncAll(self, syncFileOrDir="", remoteUser="gdlocal", remotePWD="gdlocal", remoteIP_list=[]):
		if not remoteIP_list and not isinstance( remoteIP_list, list):
			print("remoteIP_list should be type of list.")
			return None
		self.mlog.info("remote IP list:%s" %(str(remoteIP_list)))
		failIP = []
		for remoteIP in remoteIP_list:
			if not self.increSync(remoteIP, syncFileOrDir, remoteUser, remotePWD):
				failIP.append(remoteIP)
		self.mlog.info("increSyncAll failed IPs:%s" %(str(failIP)))
		return failIP

	def fullSyncAll(self, syncFileOrDir="",remoteUser="gdlocal", remotePWD="gdlocal", remoteIP_list=[]):
		if not remoteIP_list and not isinstance(remoteIP_list, list):
			print("remoteIP_list should be type of list.")
			return None
		self.mlog.info("remote IP list:%s" % (str(remoteIP_list)))
		failIP = []
		for remoteIP in remoteIP_list:
			if not self.fullSync(remoteIP, syncFileOrDir, False, remoteUser, remotePWD):
				failIP.append(remoteIP)
		self.mlog.warning("increSyncAll failed IPs:%s" % (str(failIP)))
		return failIP

	def mergeLists(self, *args):
		"""
		# 合并所有的list，自动去除相同项
		:param data_1:
		:param data_2:
		:return: merged list (set)
		"""
		if not args:
			return []
		merged_list = set()
		for item in args:
			if not item:
				continue
			for i_list in item:
				try:
					merged_list.add(tuple(i_list))
				except Exception as e:
					self.mlog.warning("item-%s added failed." % str(i_list))
					self.mlog.exception(e)
					continue

		return sorted(merged_list, key=lambda x: x[0], reverse=False)




def main():
	"""
	## Python的入口开始
	:return:
	"""
	from utils import my_logger
	mlog = my_logger("jc_rsync_tools")
	module = sys.modules[__name__]
	# getattr() 函数用于返回一个对象属性值。
	# sys.argv 是获取运行python文件的时候命令行参数,且以list形式存储参数
	# sys.argv[0] 代表当前module的名字
	try:
		func = getattr(module, sys.argv[1])
	except Exception as e:
		mlog.exception(e)
	else:
		args = None
		if len(sys.argv) > 1:
			args = sys.argv[2:]
			mlog.debug("args = %s" %args)
			func(*args)


if __name__ == "__main__":


	ipp = SyncTool()
	ipp.mlog.info("This is only test para.")

	#print(ipp.increSync("172.21.204.238", "/tmp/autopanic_ips_stats.csv", remoteUser="gdlocal", remotePWD="gdlocal"))
	#print(ipp.increSyncAll( syncFileOrDir="/tmp/autopanic_ips_stats.csv", remoteUser="gdlocal", remotePWD="gdlocal", remoteIP_list=["172.21.204.237", "172.21.204.238","172.21.204.239"]))
	#logging.critical(ipp.fullSyncAll(syncFileOrDir="/tmp/autopanic_ips_stats.csv", remoteUser="gdlocal", remotePWD="gdlocal", remoteIP_list=["172.21.204.237", "172.21.204.238", "172.21.204.239"]))

else:
	#main()
	pass
# -*- coding:utf-8 -*-
import logging

class MyLogger(object):
	"""
	# 自定义log输出器
	# 单例模式
	"""
	_instance = None
	_log_obj = None
	_log_path = None
	_instance_pool = {}
	__mlog = None
	def __new__(cls, logname, logpath="/tmp"):
		cls._log_obj = logname
		cls._log_path = logpath
		try:
			return cls._instance_pool[cls._log_obj][1]
		except:
			try:  # Python2
				cls._instance = object.__new__(cls, logname, logpath)
			except TypeError:  # Python3
				cls._instance = object.__new__(cls)
			cls._instance_pool.update({cls._log_obj:(cls._log_path, cls._instance)})
			return cls._instance

	def __init__(self, logname, logpath="/tmp"):
		pass

	def get(self):
		"""
		# 自定义log显示及输出
		:param log_obj: object name who exec logger
		:param log_path: log output filepath
		:return: logger obj
		"""
		logger = self.__mlog
		if logger:
			return logger

		logger = logging.getLogger(self._log_obj)
		# print(logger.handlers)
		logger.setLevel(logging.INFO)
		console_handle = logging.StreamHandler()
		file_handle = logging.FileHandler(filename=self._log_path + "/" +self._log_obj + ".log")
		formatter = logging.Formatter('%(asctime)s - %(name)s:%(funcName)s - %(levelname)s - %(message)s ')
		console_handle.setFormatter(formatter)
		file_handle.setFormatter(formatter)
		logger.addHandler(console_handle)
		logger.addHandler(file_handle)
		self.__mlog = logger

		return logger


if __name__ == "__main__":

	"""
	while True:
		# MyLogger 是单例模式 实现，否则每次新创建自定义logging一次都会导致log输出重复度加1
		mlog = MyLogger("test", "/tmp").mlog
		mlog.info("helloworld")
		mlog.info("testing log")
		import time
		time.sleep(3)
	"""

	mlog = MyLogger("test","/tmp").get()
	mlog.info("test")

	mlog2 = MyLogger("test", "/tmp").get()
	mlog2.info("test2")

	mlog2 = MyLogger("test2", "/tmp").get()
	mlog2.info("test2")

	mlog3 = MyLogger("test", "/tmp").get()
	mlog3.info("test3 heelowrold")

	mlog4 = MyLogger("test", "/tmp").get()
	mlog4.info("test4 heelowrold")
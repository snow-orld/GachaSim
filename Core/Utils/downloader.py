#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file 		downloader.py
@author 	Xueman Mou
@created 	2020-9-20 14:29:00 GMT +0800
@version 	$Id: downloader.py 01 2020-9-18 19:48:00 GMT +0800 $
@env 		python 3.8.4

Batch download all servants and crafts' card images and avatars/icons.
"""

import os
import workerpool
import requests
from datetime import datetime

CURDIR = os.path.dirname(__file__)
WORKER_NUM = 8

def get_options():
	parser = argparse.ArgumentParser(description='Card Image Downloader.')
	parser.add_argument('-w', '--worker', type=int, default=WORKER_NUM, help='Specify the number of workers')
	
	args = parser.parse_args()
	return args

def download(servants, crafts, worker_num=WORKER_NUM):
	"""
	Mass download images specified in imgurls.

	@param servants a list of Servants
	@param crafts a list of Crafts
	"""
	start = datetime.utcnow()

	class DownloadJob(workerpool.Job):
		def __init__(self, obj):
			self.obj = obj
		def run(self):
			try:
				self.obj.download_gacha_card_img()
			except requests.exceptions.ConnectionError:
				print('Downloading %s aborted. '\
					'UnknownProtocol(HTTP 0.0/)\nPlease try again' % self.url)
				pool.terminate()
				pool.join()
			except KeyboardInterrupt:
				print('Called KeyboardInterrupt, terminaing workers')
				pool.terminate()
				pool.join()

	pool = workerpool.WorkerPool(size=worker_num, maxjobs=worker_num)
	for obj in servants + crafts:
		job = DownloadJob(obj)
		pool.put(job)

	# Send shutdown jobs to all threads, and wait until all the jobs have been completed
	pool.shutdown()
	pool.wait()
	del pool

	end = datetime.utcnow()
	print('Downloaded %d card images in: %s' % \
		((len(servants) + len(crafts)) * 2, abs(end - start)))


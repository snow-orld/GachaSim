#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file 		pool.py
@author 	Xueman Mou
@created 	2020-9-15 15:31:00 GMT +0800
@version 	$Id: pool.py 01 2020-9-15 15:31:00 GMT +0800 $
@env 		python 3.8.4

Class Card Pool.
"""

class Pool(object):
	"""
	Class Pool for gacha.

	@attr id the unique pool identification
	@attr startDate the starting date of the pool, including date and time
	@attr duration the number of days when the pool is open
	@attr rates a dictionary of drawing rates for each type of card
	"""
	def __init__(self, id, startDate, openDays, rates):
		super(Pool, self).__init__()
		self.id = id
		self.startDate = startDate
		self.endDate = startDate + openDays
		self.rates = rates

	def draw(self):
		"""The gacha core."""
		pass
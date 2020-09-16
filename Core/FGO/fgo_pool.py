#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file 		fgo_pool.py
@author 	Xueman Mou
@created 	2020-9-15 15:59:00 GMT +0800
@version 	$Id: fgo_pool.py 01 2020-9-15 15:59:00 GMT +0800 $
@env 		python 3.8.4

Class Card Pool in FGO.
"""

from ..Base.pool import Pool

class FGOPool(Pool):
	"""
	FGO pool.

	@attr inherit all attributes from Pool.
	@attr poolType the type of the pool, either story or rate-up temporary pool
	@attr name the descriptive pool name
	"""
	def __init__(self, id, poolType, name, startDate, openDays, rates):
		super(FGOPool, self).__init__(id, startDate, openDays, rates)
		self.type = poolType
		self.name = name
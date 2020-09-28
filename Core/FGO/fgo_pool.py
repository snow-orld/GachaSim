#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file 		fgo_pool.py
@author 	Xueman Mou
@created 	2020-9-15 15:59:00 GMT +0800
@version 	$Id: fgo_pool.py 01 2020-9-27 15:59:00 GMT +0800 $
@env 		python 3.8.4

Class Card Pool in FGO.
"""

import random
from ..Base.pool import Pool

golden_rate_group = {"svt5": 1, "svt4": 3, "svt3": 0, "ce5": 4, "ce4": 92, "ce3": 0}
servant_rate_group = {"svt5": 1, "svt4": 3, "svt3": 96, "ce5": 0, "ce4": 0, "ce3": 0}

class FGOSinglePool(Pool):
	"""
	FGO single pool. The actual pool that will appear at one specific time.

	@attr inherit all attributes from Pool.
			Note: here id is is from the parent FGOPool. Its key is (id, name).
	@attr name_list the list of servant names' combination that as rate-ups
			during the pool's open duration.
	@attr rates a dictionary of gacha rates for each
	"""
	def __init__(self, id, name, start_date, open_days, rates):
		super(FGOSinglePool, self).__init__('FGO', id, start_date,
		                                    open_days, rates)
		self.name = name

class FGOPool(object):
	"""
	FGO pool. A collection of single pools that is open for a fixed duration.

	@attr id the unique identifier of this pool
	@attr start_date
	@attr end_date
	@attr rates a dictionary of upped servant name combination's gacha rate
	"""
	def __init__(self, id, pool_name, start_date, open_days,
	             name_list, rates_str):
		super(FGOPool, self).__init__()
		self.id = id
		self.pool_name = pool_name
		self.start_date = start_date
		self.end_date = start_date + open_days
		self.rates = self.rate_parser(name_list, rates_str)
		self.pool_collection = self.pool_parser(self.rates)

	def __repr__(self):
		string = "Pool #%d %s has " % (self.id, self.pool_name)
		string += "%d daily-ups " % len(self.pool_collection)
		string += "(%s - %s):\n" % (self.start_date, self.end_date)
		for i, pool in enumerate(self.pool_collection):
			string += "%d - %s \n" % (i, pool.name)
			for rate in pool.rates:
				string += "  %s\n" % rate
		return string

	def table_parser(self, raw_str, delimiter):
		"""
		Parse raw string in table format.
		NOTE: All fields are of string type.
		"""
		datas = []
		lines = raw_str.split('\n')
		keys = [key.strip() for key in lines[0].split(delimiter)]

		for line in lines[1:]:
			data = {}
			for i, field in enumerate(line.split(delimiter)):
				data[keys[i]] = field.strip()
			datas.append(data)
		return datas

	def rate_parser(self, name_list, rates_str):
		"""
		@para name_list the list of servant name combinations for each
			daily-change single pool
		@para rates_str the list of rates raw string for each up-pair
		@return a dictionary with upped servant name combination as key,
			corresponding pool data dictionary (as defined in
			web/GacahTest.html) as value.
		"""
		rates = {}
		for name, rate_str in zip(name_list, rates_str):
			rates[name] = self.table_parser(rate_str, "\t")
			for i in range(len(rates[name])):
				ids_data = rates[name][i]['ids'].split(',')
				rates[name][i]['ids'] = [int(id.strip()) for id in ids_data]
				rates[name][i]['weight'] = float(rates[name][i]['weight'])
		return rates

	def pool_parser(self, rates):
		"""Generate collection of pools from rate raw string."""
		collection = []
		for name, rate in rates.items():
			pool = FGOSinglePool(self.id, name, self.start_date,
			                     self.end_date - self.start_date, rate)
			collection.append(pool)
		return collection

	# NOTE: the following summon functions do not maintain global variables
	# such as quartz, summon types, history summon results.
	def summon1(self, pool_id):
		assert pool_id in range(len(self.pool_collection)), \
			"Pool id %d overflow (%d)." % (pool_id, len(self.pool_collection))
		return self.pool_collection[pool_id].gacha_roll()

	def summon10(self, pool_id):
		assert pool_id in range(len(self.pool_collection)), \
			"Pool id %d overflow (%d)." % (pool_id, len(self.pool_collection))
		pool = self.pool_collection[pool_id]
		res = [pool.gacha_roll(golden_rate_group),
		       pool.gacha_roll(servant_rate_group)]
		for i in range(11 - 2):
			res.append(pool.gacha_roll())
		return random.sample(res, k=len(res))

	def summon10ssr(self, pool_id):
		assert pool_id in range(len(self.pool_collection)), \
			"Pool id %d overflow (%d)." % (pool_id, len(self.pool_collection))
		pool = self.pool_collection[pool_id]
		res = [pool.gacha_roll({"svt5": 100, "svt4": 0, "svt3": 0,
		                        "ce5": 0, "ce4": 0, "ce3": 0}),
		       pool.gacha_roll(golden_rate_group),
		       pool.gacha_roll(servant_rate_group)]
		for i in range(11 - 3):
			res.append(pool.gacha_roll())
		return random.sample(res, k=len(res))

	def summon10ssrsr(self, pool_id):
		assert pool_id in range(len(self.pool_collection)), \
			"Pool id %d overflow (%d)." % (pool_id, len(self.pool_collection))
		pool = self.pool_collection[pool_id]
		res = [pool.gacha_roll({"svt5": 100, "svt4": 0, "svt3": 0,
		                        "ce5": 0, "ce4": 0, "ce3": 0}),
		       pool.gacha_roll({"svt5": 1, "svt4": 99, "svt3": 0,
		                        "ce5": 0, "ce4": 0, "ce3": 0}),
		       pool.gacha_roll(golden_rate_group),
		       pool.gacha_roll(servant_rate_group)]
		for i in range(11 - 4):
			res.append(pool.gacha_roll())
		return random.sample(res, k=len(res))


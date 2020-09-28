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

import random

class RollResult(object):
	"""
	Gacha roll's result for once.

	@attr type card type
	@attr star card star/rank
	@attr id the id of that card type
	"""
	def __init__(self, card_type, star, id):
		self.type = card_type
		self.star = star
		self.id = id

	def __repr__(self):
		return 'Card(%s%s #%d)' % (self.type, self.star, self.id)

class Pool(object):
	"""
	Class Pool for gacha.

	@attr game the game name
	@attr id the unique pool identification
	@attr start_date the starting date of the pool, including date and time
	@attr end_date the ending date of the pool
	@attr rates an array of dictionaries of gacha rates for each group of cards
	"""
	def __init__(self, game, id, start_date, open_days, rates):
		super(Pool, self).__init__()
		self.game = game
		self.id = id
		self.start_date = start_date
		self.end_date = start_date + open_days
		self.rates = rates

	def gacha_roll(self, rate_group=None):
		"""
		The gacha core.

		@attr rate_group extra rates that control each card type appearance
		"""
		assert self.game.lower() == 'fgo', 'Gacha for Game %s is not ' \
		                                   'supported yet.' % self.game.title()
		# For each type, calculate total rate for the type
		type_weight_sum = {}
		for rate in self.rates:
			card_type = rate['type'] + rate['star']
			value = type_weight_sum.get(card_type, 0)
			type_weight_sum[card_type] = value + float(rate['weight'])

		# Initialize the coefficients for each card type, default to 1,
		# i.e. no change on original pool's rate
		coeffs = {}
		for card_type in type_weight_sum:
			coeffs[card_type] = 1.0
			# Calculate coefficients that multiply to the pool's rates, used
			# for different summon (whether only ssr or sr or both)
			if rate_group:
				coeffs[card_type] = rate_group[card_type] \
				                    / type_weight_sum[card_type] \
					if type_weight_sum[card_type] >= 0.0001 else 1.0

		weight_sum = 0
		for rate in self.rates:
			weight_sum += rate['weight'] * coeffs[
				rate['type'] + rate['star']]

		rnd = random.random()
		weight_accu = 0
		for rate in self.rates:
			weight_accu += rate['weight'] * coeffs[
				rate['type'] + rate['star']]
			if rnd <= weight_accu / weight_sum:
				res_rate = rate
				break

		res = RollResult(res_rate['type'], res_rate['star'],
		                 random.choice(res_rate['ids']))

		return res
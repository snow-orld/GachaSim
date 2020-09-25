#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file 		fgo_craft.py
@author 	Xueman Mou
@created 	2020-9-15 15:48:00 GMT +0800
@version 	$Id: fgo_craft.py 01 2020-9-15 15:48:00 GMT +0800 $
@env 		python 3.8.4

Class Essence Craft, a special kind of FGO Card.
"""

from .fgo_card import FGOCard

class Craft(FGOCard):
	"""
	Class Essence Craft, a special kind of FGO Card.
	"""
	def __init__(self, id, star, name, name_link, cost, hp1, hpmax, \
		         atk1, atkmax, des, des_max, icon, img_link):
		super(Craft, self).__init__('craft', int(id), star, name, img_link, icon)
		self.star = int(star)
		self.name_cn = name
		self.name_link = name_link
		self.cost = cost
		self.hp1 = hp1
		self.hpmax = hpmax
		self.atk1 = atk1
		self.atkmax = atkmax
		self.des = des
		self.des_max = des_max
		self.icon = icon
		self.img_link = img_link

	def show(self, wait=0):
		window_name = '%s %03d' % (self.card_type, self.id)
		super(Craft, self).show(window_name=window_name, wait=wait)
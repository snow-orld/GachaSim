#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file 		fgo_servant.py
@author 	Xueman Mou
@created 	2020-9-15 16:35:00 GMT +0800
@version 	$Id: fgo_servant.py 01 2020-9-15 16:35:00 GMT +0800 $
@env 		python 3.8.4

Class Servant, a special kind of FGO Card.
"""

from .fgo_card import FGOCard

class Servant(FGOCard):
	"""
	FGO Servant.
	"""
	def __init__(self, id, star, name_cn, name_jp, name_en, name_link, \
		         name_other, cost, faction, get, hp, atk, class_link, \
		         avatar, np_type, img_links):
		super(Servant, self).__init__('servant', int(id), len(star), name_cn, \
			  img_links[0], avatar)
		self.star = len(star)
		self.name_cn = name_cn
		self.name_jp = name_jp
		self.name_en = name_en
		self.name_link = name_link
		self.name_other = name_other
		self.cost = cost
		self.faction = faction
		self.get = get
		self.hp = hp
		self.atk = atk
		self.class_link = class_link
		self.avatar = avatar
		self.np_type = np_type
		self.img_links = img_links
		self.img_file = None

	def show(self, wait=0):
		super(Servant, self).show(window_name=self.name_en, wait=wait)

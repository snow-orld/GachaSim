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
	def __init__(self, id, star, name):
		super(Craft, self).__init__('FGO', id, star, 'craft', name, '2016-10-24', '.')

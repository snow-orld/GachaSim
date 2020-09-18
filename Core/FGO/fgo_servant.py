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
	def __init__(self, id, star, name_cn, name_jp, name_en, name_link, name_other, cost, \
		faction, get, hp, atk, class_link, avatar, card1, card2, card3, \
		card4, card5, np_card, np_type, class_icon, stars_marker, class_marker, \
		get_marker, cards_marker, npc_marker, npt_marker, fac_marker, \
		sex_marker, prop1_marker, prop2_marker, traits_marker, sort_atk, \
		sort_hp):
		# Fetch the card img used to display during gachaing then call the parent's init

		super(Servant, self).__init__('servant', id, len(star), name_cn)
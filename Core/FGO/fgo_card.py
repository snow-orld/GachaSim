#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file 		fgo_card.py
@author 	Xueman Mou
@created 	2020-9-14 13:44:00 GMT +0800
@version 	$Id: fgo_card.py 01 2020-9-14 13:44:00 GMT +0800 $
@env 		python 3.8.4

Class Card in FGO.
"""

import cv2
from ..Base.card import Card

class FGOCard(Card):
	"""
	FGO Card.

	@attr inherit all attributes defined in Card

	@attr card_type the card type, whether it is a servant or an essence craft
	@attr name_cn the name_cn that appears on the card
	"""
	def __init__(self, card_type, id, star, name_cn, img_link):
		super(FGOCard, self).__init__('FGO', id, star, img_link)
		self.__card_type = card_type.lower()
		self.__name_cn = name_cn

	def is_valid(self):
		return self.__card_type.lower() in ['servant', 'craft'] and \
				self.__rank in range(1, 6)

	def __repr__(self):
		pass

if __name__ == '__main__':
	fgoCard = FGOCard('Servant', 1, 4, 0, '.')

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

	@attr type the card type, whether it is a servant or an essence craft
	@attr name the name that appears on the card
	"""
	def __init__(self, game, id, rank, type, name, releaseDate, imgLink):
		super(FGOCard, self).__init__(game, id, rank, releaseDate, imgLink)
		self.type = type
		self.name = name

	def __repr__(self):
		pass

if __name__ == '__main__':
	fgoCard = FGOCard('FGO', 0, 'SSR', 'Servant', 0, '2020-9-15', '.')

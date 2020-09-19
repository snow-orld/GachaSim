#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file 		card.py
@author 	Xueman Mou
@created 	2020-9-14 13:44:00 GMT +0800
@version 	$Id: card.py 01 2020-9-14 13:44:00 GMT +0800 $
@env 		python 3.8.4

Class Card.
"""

class Card(object):
	"""
	Card class for gacha.

	@attr id the card unique identifier number
	@attr rank the rareness rank of the card. differs in different games.
	@attr card_img the path to the image of the card. can be either local path or url.
	@attr game the game name to which the card belongs
	"""
	def __init__(self, game, id, rank, card_img_link):
		super(Card, self).__init__()
		self.id = id
		self.rank = rank
		self.img_link = card_img_link
		self.game = game

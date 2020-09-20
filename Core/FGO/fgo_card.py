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

import os
import cv2
import requests
from ..Base.card import Card

CURDIR = os.path.dirname(__file__)

class FGOCard(Card):
	"""
	FGO Card.

	@attr inherit all attributes defined in Card

	@attr card_type the card type, whether it is a servant or an essence craft
	@attr name_cn the name_cn that appears on the card
	"""
	def __init__(self, card_type, id, star, name_cn, img_link, avatar_link):
		super(FGOCard, self).__init__('FGO', id, star, img_link, avatar_link)
		self.card_type = card_type.title()
		self.name_cn = name_cn

	def is_valid(self):
		return self.card_type.lower() in ['servant', 'craft'] and \
				self.rank in range(1, 6)

	def __repr__(self):
		pass

	def download_gacha_card_img(self):
		img_folder = os.path.join(CURDIR, '../../Assets/Images/FGO/%s' \
			% self.card_type)
		if not os.path.exists(img_folder):
			os.makedirs(img_folder)
		
		img_file = os.path.join(img_folder, '%03d.%s.png' \
			% (self.id, self.name_cn.replace('/', '-')))
		avatar_file = img_file.replace('.png', '_avatar.png')
		if not os.path.exists(img_file):
			print('Downloading %s ...' % os.path.relpath(img_file))
			r = requests.get(self.img_link)
			with open(img_file, 'wb') as f:
				f.write(r.content)
		else:
			print('Phase 1 image of %s already exists.' % self.name_cn)
		if not os.path.exists(avatar_file):
			print('Downloading %s ...' % os.path.relpath(avatar_file))
			r = requests.get(self.avatar_link)
			with open(avatar_file, 'wb') as f:
				f.write(r.content)
		else:
			print('Avatar image of %s already exists.' % self.name_cn)
	
		return avatar_file, img_file

	def show(self, window_name, wait=0):
		self.avatar_file, self.img_file = self.download_gacha_card_img()
		img = cv2.imread(self.img_file)
		cv2.imshow(window_name, img)
		img = cv2.imread(self.avatar_file)
		cv2.imshow(window_name + ' avatar', img)
		cv2.waitKey(wait)

if __name__ == '__main__':
	fgoCard = FGOCard('Servant', 1, 4, 0, '.')

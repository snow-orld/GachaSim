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
import sys
import cv2
import requests
import pathlib
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

		self.local_img_folder = os.path.join(CURDIR, '..', '..', 'Assets', \
			'Images', 'FGO', self.card_type)
		self.local_img = os.path.join(self.local_img_folder, '%03d.%s.png' \
			% (self.id, self.name_cn))
		# Handle error that opencv won't open the Windows path to number
		# starting file name. Still cannot read the img from file after
		# modifying the relpath of local img to posix.
		self.local_img = pathlib.Path(os.path.relpath(self.local_img)).as_posix()
		self.local_avatar = self.local_img.replace('.png', '_avatar.png')

		if not os.path.exists(self.local_img) or \
				not os.path.exists(self.local_avatar):
			self.download_gacha_card_img(verbose=True)

	def is_valid(self):
		return self.card_type.lower() in ['servant', 'craft'] and \
				self.rank in range(1, 6)

	def __repr__(self):
		return '%s %s %d %s' % \
		       (self.game, self.card_type, self.id, self.name_cn)

	def download_gacha_card_img(self, verbose=False):
		img_folder = self.local_img_folder
		if not os.path.exists(img_folder):
			os.makedirs(img_folder)
		img_file = self.local_img
		avatar_file = self.local_avatar
		if not os.path.exists(img_file):
			print('Downloading %s ...' % os.path.relpath(img_file))
			r = requests.get(self.img_link)
			with open(img_file, 'wb') as f:
				f.write(r.content)
		else:
			if verbose:
				print('%s\' card image already exists.' % self.name_cn)
		if not os.path.exists(avatar_file):
			print('Downloading %s ...' % os.path.relpath(avatar_file))
			r = requests.get(self.avatar_link)
			with open(avatar_file, 'wb') as f:
				f.write(r.content)
		else:
			if verbose:
				print('%s\'s card avatar already exists.' % self.name_cn)

		return avatar_file, img_file

	def show(self, window_name, wait=0):
		print('localimg %s\nlocalavatar %s' % (self.local_img, self.local_avatar))
		print('localimg exists? %s' % os.path.exists(self.local_img))
		img = cv2.imread(self.local_img)
		cv2.imshow(window_name, img)
		img = cv2.imread(self.local_avatar)
		cv2.imshow(window_name + ' avatar', img)
		cv2.waitKey(wait)

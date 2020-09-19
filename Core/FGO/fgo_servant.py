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

import os
import cv2
import urllib.request
import requests
from .fgo_card import FGOCard

CURDIR = os.path.dirname(__file__)

class Servant(FGOCard):
	"""
	FGO Servant.
	"""
	def __init__(self, id, star, name_cn, name_jp, name_en, name_link, \
		         name_other, cost, faction, get, hp, atk, class_link, \
		         avatar, np_type, img_links):
		super(Servant, self).__init__('servant', int(id), len(star), name_cn, img_links[0])
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

	def download_1st_phase_img(self):
		img_folder = os.path.join(CURDIR, '../../Assets/Images/FGO/Servant')
		if not os.path.exists(img_folder):
			os.makedirs(img_folder)
		img_file = os.path.join(img_folder, '%03d.%s.png' \
			% (self.id, self.name_cn))
		if not os.path.exists(img_file):
			print('Downloading %s ...' % os.path.relpath(img_file))
			r = requests.get(self.img_link)
			with open(img_file, 'wb') as f:
				f.write(r.content)
		else:
			print('Phase 1 image of %s already exists.' % self.name_cn)
		return img_file

	def show(self):
		self.img_file = self.download_1st_phase_img()
		img = cv2.imread(self.img_file)
		cv2.imshow(self.name_en, img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
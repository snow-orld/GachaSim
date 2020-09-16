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
	def __init__(self, id, rank, name):
		super(Servant, self).__init__('FGO', id, rank, 'servant', name, '2016-10-25')
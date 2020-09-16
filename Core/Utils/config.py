#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file 		config.py
@author 	Xueman Mou
@created 	2020-9-14 14:09:00 GMT +0800
@version 	$Id: config.py 01 2020-9-14 14:09:00 GMT +0800 $
@env 		python 3.8.4

Read configuration json files to set up the environment of the game.
"""

import os, sys
import re
import json

CURDIR = os.path.dirname(__file__)

def readConf():
	"""Read from config file to load details of a game."""
	confFile = os.path.join(CURDIR, '../../Config/conf.json')
	with open(confFile, 'r') as f:
		game = json.load(f)['game']
	gameConfFile = os.path.join(CURDIR, '../../Config/conf_%s.json' % game.lower())
	with open(gameConfFile, 'r') as f:
		return json.load(f)

if __name__ == '__main__':
	conf = readConf()
	print(conf)
#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file 		parser.py
@author 	Xueman Mou
@created 	2020-9-17 13:05:00 GMT +0800
@version 	$Id: parser.py 01 2020-9-18 19:48:00 GMT +0800 $
@env 		python 3.8.4

Parse fetched data in format of lines, each of which is describing brief
info about one servant in the list.
"""

import os, sys
import codecs

print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(
		__file__, __name__,str(__package__)))
from ..FGO.fgo_servant import Servant

CURDIR = os.path.dirname(__file__)

def write_header(header, is_servant=True):
	"""
	Save data header fields to tmp, templating code writing when using the
	field name as variable names.

	@para header the split header fields from the first line of data
	@para is_servant whether the header is for servant (1) or craft (0)
	"""
	# Get a template for extracted header fields as vars
	tmp_dir = os.path.join(CURDIR, '../../tmp')
	suffix = '英灵' if is_servant else '礼装'
	tmp_file = os.path.join(tmp_dir, 'header_%s.txt' % suffix)
	if not os.path.exists(tmp_dir):
		os.makedirs(tmp_dir)
	with codecs.open(tmp_file, 'w') as f:
		string = ''
		for i, field in enumerate(header):
			string = '%s%s%s' % (string, field, ', ' if i < len(header) - 1 else '')
			if len(string) > 80 - 20:
				f.write('%s\\\n' % string)
				string = ''
		f.write(string + '\n\n')
		for i, field in enumerate(header):
			f.write('%s%s' % (field, ', ' if i < len(header) - 1 else ''))
		f.write('\n\n')
		for i, field in enumerate(header):
			f.write('self.%s = %s\n' % (field, field))

def parse_servant(lines):
	"""
	Parse multiple servants' brief info from fetched data of 英灵图鉴.html.

	@return list of Servant objects, sorted by servant id.
	"""
	servants = []

	header = lines[0].rstrip().split(',')
	write_header(header, is_servant=True)

	for line in lines[1:]:
		id, star, name_cn, name_jp, name_en, name_link, name_other, cost, \
		faction, get, hp, atk, class_link, avatar, card1, card2, card3, \
		card4, card5, np_card, np_type, class_icon, stars_marker, class_marker, \
		get_marker, cards_marker, npc_marker, npt_marker, fac_marker, \
		sex_marker, prop1_marker, prop2_marker, traits_marker, sort_atk, \
		sort_hp = line.rstrip().split(',')

		print('Servant %03d: %s %s %s avatar %s hp %s atk %s '\
			'np_type %s class_icon %s sort_atk %s sort_hp %s' % 
			(int(id), name_cn, name_link, class_link, avatar, hp, atk,
			np_type, class_icon, sort_atk, sort_hp))

		servant = Servant(id, star, name_cn, name_jp, name_en, name_link, \
		                  name_other, cost, faction, get, hp, atk, class_link, \
		                  avatar, np_type)
		break

	return servants

def parse_craft(lines):
	"""
	Parse multiple craft essences' brief info from fetched data of 礼装图鉴.html.

	@return list of Craft objects, sorted by craft essence id.
	"""
	pass

def main():
	names = ['英灵图鉴', '礼装图鉴']
	for name in names:
		file = os.path.join(CURDIR, '../../csv/%s.csv' % name)
		with codecs.open(file, 'r', encoding='utf-8') as f:
			lines = f.readlines()
			if name == '英灵图鉴':
				parse_servant(lines)
			else:
				parse_craft(lines)

if __name__ == '__main__':
	main()
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
from tqdm import tqdm
from datetime import datetime

print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(
		__file__, __name__,str(__package__)))
from .config import read_conf
from .crawler import fetch_servant_card_images, fetch_craft_card_images
from .downloader import download
from ..FGO.fgo_servant import Servant
from ..FGO.fgo_craft import Craft

CURDIR = os.path.dirname(__file__)
GAMECONF = read_conf()

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
			string = '%s%s%s' % (string, field, \
				', ' if i < len(header) - 1 else '')
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
	# write_header(header, is_servant=True)

	for line in tqdm(lines[1:]):
		id, star, name_cn, name_jp, name_en, name_link, name_other, cost, \
		faction, get, hp, atk, class_link, avatar, card1, card2, card3, \
		card4, card5, np_card, np_type, class_icon, stars_marker, class_marker, \
		get_marker, cards_marker, npc_marker, npt_marker, fac_marker, \
		sex_marker, prop1_marker, prop2_marker, traits_marker, sort_atk, \
		sort_hp = line.rstrip().split(',')

		# print('Servant %03d: %s %s %s avatar %s hp %s atk %s '\
		# 	'np_type %s class_icon %s sort_atk %s sort_hp %s' % 
		# 	(int(id), name_cn, name_link, class_link, avatar, hp, atk,
		# 	np_type, class_icon, sort_atk, sort_hp))

		img_links = fetch_servant_card_images(name_link, GAMECONF['use_cache'])
		avatar = os.path.join(GAMECONF['url_img_root'], avatar.lstrip('/'))

		# 所罗门页面没有graphpicker，当然他也不在卡池里
		if img_links == None:
			continue

		servant = Servant(id, star, name_cn, name_jp, name_en, name_link, \
		                  name_other, cost, faction, get, hp, atk, class_link, \
		                  avatar, np_type, img_links)
		servants.append(servant)

	return servants

def parse_craft(lines):
	"""
	Parse multiple craft essences' brief info from fetched data of 礼装图鉴.html.

	@return list of Craft objects, sorted by craft essence id.
	"""
	crafts = []

	header = lines[0].rstrip().split(',')
	write_header(header, is_servant=False)

	for line in tqdm(lines[1:]):
		id, star, star_str, name, name_link, name_other, cost, hp1, hpmax, \
		atk1, atkmax, des, des_max, icon, icon_eff, type_marker, stars_marker, \
		stats_marker, sort_atk, sort_hp = line.rstrip().split(',')

		# print('Craft %03d: %s %s %s hp1 %s hpmax %s atk1 %s atkmax %s ' \
		# 	'des %s des_max %s type_marker %s' % 
		# 	(int(id), star_str, name, name_link, hp1, hpmax, atk1, atkmax,
		# 		des, des_max, type_marker))

		# Craft 361-366 contains half-corner ':' in name but full-corner '：' in
		# name_link. And the later is used to name the local image to avoid
		# naming restriction with ':'.
		name = name.replace(':', '：').replace('/', '-')

		img_link = fetch_craft_card_images(name_link, GAMECONF['use_cache'])
		icon = os.path.join(GAMECONF['url_img_root'], icon.lstrip('/'))

		craft = Craft(id, star, name, name_link, cost, hp1, hpmax, \
		         atk1, atkmax, des, des_max, icon, img_link)
		crafts.append(craft)

	return crafts

def parse_from_html():
	"""
	Parse from previously cached .csv files containing summary info of servant and craft.
	Extra work of extracting card image link from individual
	Return servant object, and craft object lists.
	"""
	s = datetime.utcnow()

	names = ['英灵图鉴', '礼装图鉴']
	servants = []
	crafts = []
	for name in names:
		file = os.path.join(CURDIR, '../../csv/%s.csv' % name)
		with codecs.open(file, 'r', encoding='utf-8') as f:
			lines = f.readlines()
			if name == '英灵图鉴':
				servants = parse_servant(lines)
			else:
				crafts = parse_craft(lines)

	e = datetime.utcnow()
	print('Parsing servants and crafts from html files costs: %s' % (e - s))

	return servants, crafts

def write_whole_info(servants, crafts):
	"""
	Write parsed servants' and crafts' objects to local csv file, with only
	info recorded in the class of Servant and Craft.
	"""
	print('Writing class data to files ...')
	csv_folder = os.path.join(CURDIR, '../../csv')
	if not os.path.exists(csv_folder):
		os.makedirs(csv_folder)
	servant_file = os.path.join(csv_folder, 'Servants.csv')
	craft_file = os.path.join(csv_folder, 'Crafts.csv')
	with codecs.open(servant_file, 'w', encoding='utf-8') as f:
		f.write('id,star,name_cn,name_jp,name_en,name_link,' \
				'name_other,cost,faction,get,hp,atk,class_link,' \
				'avatar,np_type,img_links\n')
		for servant in servants:
			str_format = '%d,%d,'+'%s,'*13
			f.write(str_format % \
					(servant.id, servant.star, servant.name_cn, servant.name_jp,\
					 servant.name_en, servant.name_link, servant.name_other,\
					 servant.cost, servant.faction, servant.get, servant.hp,\
					 servant.atk, servant.class_link, servant.avatar, \
					 servant.np_type))
			f.write('%s\n' % str(servant.img_links).replace(',','\t').\
			        replace(' ', ''))

	with codecs.open(craft_file, 'w', encoding='utf-8') as f:
		f.write('id,star,name,name_link,cost,hp1,hpmax,' \
		        'atk1,atkmax,des,des_max,icon,img_link\n')
		for craft in crafts:
			str_format = '%d,%d,'+'%s,'*10+'%s\n'
			f.write(str_format % \
					(craft.id, craft.star, craft.name_cn, craft.name_link, \
					 craft.cost, craft.hp1, craft.hpmax, craft.atk1, \
					 craft.atkmax, craft.des, craft.des_max, craft.icon, \
					 craft.img_link))

def parse_from_csv():
	"""
	Parse data from previously re-written .csv files, which append img_links
	info at the end of each line in original .csv files directly generated
	from '英灵图鉴', '礼装图鉴' pages.
	"""
	s = datetime.utcnow()

	csv_folder = os.path.join(CURDIR, '../../csv')
	servant_file = os.path.join(csv_folder, 'Servants.csv')
	craft_file = os.path.join(csv_folder, 'Crafts.csv')
	if not os.path.exists(servant_file) or not os.path.exists(craft_file) or \
		os.stat(servant_file).st_size == 0 or os.stat(craft_file).st_size == 0:
		servants, crafts = parse_from_html()
		write_whole_info(servants, crafts)
	else:
		servants = []
		crafts = []
		with codecs.open(servant_file, 'r', encoding='utf-8') as f:
			print('Reading Servants from %s ...' % os.path.relpath(servant_file))
			for line in tqdm(f.readlines()[1:]):
				id, star, name_cn, name_jp, name_en, name_link, \
				name_other, cost, faction, get, hp, atk, class_link, \
				avatar, np_type, img_links = line.split(',')
				img_links = img_links.replace('\t', ',')
				img_links = img_links.replace('\'', '')
				img_links = img_links.split(']')[0].split('[')[-1]
				img_links = img_links.split(',')
				servant = Servant(id, star, name_cn, name_jp, name_en, \
							name_link, name_other, cost, faction, get, \
							hp, atk, class_link, avatar, np_type, img_links)
				servants.append(servant)

		with codecs.open(craft_file, 'r', encoding='utf-8') as f:
			print('Reading Crafts from %s ...' % os.path.relpath(craft_file))
			for line in tqdm(f.readlines()[1:]):
				id, star, name, name_link, cost, hp1, hpmax, atk1, atkmax, \
				des, des_max, icon, img_link = line.split(',')
				craft = Craft(id, star, name, name_link, cost, hp1, hpmax, \
							atk1, atkmax, des, des_max, icon, img_link)
				crafts.append(craft)

	e = datetime.utcnow()
	print('Parsing servants and crafts from csv files costs: %s' % (e - s))

	return servants, crafts

def main():
	servants, crafts = parse_from_csv()
	print('Loaded %d servants, %d crafts' % (len(servants), len(crafts)))
	servants[0].show()

if __name__ == '__main__':
	main()
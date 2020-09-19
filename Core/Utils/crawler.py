#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file 		crawler.py
@author 	Xueman Mou
@created 	2020-9-15 17:00:00 GMT +0800
@version 	$Id: crawler.py 01 2020-9-15 17:00:00 GMT +0800 $
@env 		python 3.8.4

Fetch servant details from fgo.wiki.

Ref: https://www.codementor.io/@codementorteam/how-to-scrape-an-ajax-website-using-python-qw8fuitvi
"""

import os, sys
import requests
import codecs
import platform
if platform.system() != 'Windows':
	from requests_html import HTMLSession
from datetime import date, datetime, timezone, timedelta
import pytz, tzlocal
import re
from bs4 import BeautifulSoup
import cv2

from .config import read_conf

CURDIR = os.path.dirname(__file__)
GAMECONF = read_conf()
UTC = timezone.utc
CST = pytz.timezone('Asia/Shanghai')
# datetime.timezone, not work with tz convertion
LOCALTZ = datetime.now(timezone(timedelta(0))).astimezone().tzinfo
# pytz.timezone
LOCALTZ = tzlocal.get_localzone()

def send_requests(name, renderJS=False):
	"""
	Get response object from sent requests to remote fgo.wiki/w/name.

	@param name the relative url of target url to fgo.wiki/w/
	@param renderJS whether to render js driven websites
	@return r the oringal or js rendered response of sent requensts
	"""
	if not renderJS:
		get = requests.get
		ConnectionError = requests.exceptions.ConnectionError
	else:
		session = HTMLSession()
		get = session.get
	try:
		url = os.path.join(GAMECONF['url_webpage_root'], name)
		r = get(url, stream=True)
	except:
		if not os.path.exists(file):
			print('Connection Failed. Please try again later to get %s.' % name)
	else:
		if renderJS:
			r.html.render()
	
	return r

def download_page(name, renderJS=False):
	"""
	Dowanload the remote webpage to local web file.

	@param name the relative url to webpage root fgo.wiki/w/
	@param renderJS whether to render js driven websites
	@return the downloaded file's path
	"""

	webfolder = os.path.join(CURDIR, '../../web')
	if not os.path.exists(webfolder):
		os.makedirs(webfolder)
	file = os.path.join(webfolder, '%s%s.html' 
		 % (name.replace('/','-'), '_rendered' if renderJS else ''))
	if os.path.exists(file):
		file_mtime_local = datetime.fromtimestamp(os.path.getmtime(file))
		file_mtime_local = LOCALTZ.localize(file_mtime_local)
	else:
		file_mtime_local = LOCALTZ.localize(datetime.now())

	if os.path.exists(file):
		print('%s already exists ...' % os.path.relpath(file))
	# Windows is internet access restricted
	if platform.system() == 'Windows':
		print('Restricted internet access to check latest %s.' % name)
		return file

	r = send_requests(name, renderJS)

	# Use the <li id="footer-info-lastmod"> tag to identify the
	# last modified time
	try:
		reg = r'<li id="footer-info-lastmod">.*(\d{4})年(\d{1,2})月(\d{1,2})日' \
		      r'\D*(\d{1,2}):(\d{1,2}).*</li>'
		y, m, d, H, M = [int(i) for i in re.search(reg, r.text).groups()]
		lastmod = '%i %i %i %i:%i:00 CST' % (d, m, y, H, M)
		lastmod_cst = datetime.strptime(lastmod, '%d %m %Y %H:%M:%S %Z')
		lastmod_cst = CST.localize(lastmod_cst)
	except AttributeError:
		lastmod_cst = file_mtime_local

	# print('File mod time %s %s' % (file_mtime_local.tzname(), file_mtime_local))
	# print('Web mod time %s %s' % (lastmod_cst.tzname(), lastmod_cst))

	if not os.path.exists(file) or os.stat(file).st_size == 0 \
		or  file_mtime_local < lastmod_cst:
		with codecs.open(file, 'w', encoding='utf-8') as f:
			print('Updating %s ...' % os.path.basename(file))
			f.write(r.text)

	return file

def fetch_html_text(name, online=True, renderJS=False):
	"""
	According to given sub url's name appended after fgo.wiki/w/, get the list
	data of either sevant or craft as a html text.

	@param name the relative url of target url to fgo.wiki/w/
	@param online whether get the text only using internet access without cache
	@param renderJS whether to render js driven websites
	@return r the oringal or js rendered response of sent requensts
	"""
	if online:
		url = os.path.join(GAMECONF['url_webpage_root'], name)
		print('Reading %s ...' % url)
		r = send_requests(name, renderJS)
		return r.text
	else:
		print('Reading cached data: ', end='')
		file = download_page(name, renderJS)
		with codecs.open(file, 'r', encoding='utf-8') as f:
			return f.read()

def fetch_csv_data(name, online=True, renderJS=False):
	"""
	Since all data is contained in the get_csv() function in the original html,
	the only left to do is to extract the raw string from the function.

	@param name the relative url of target url to fgo.wiki/w/
	@param online whether get the text only using internet access without cache
	@param renderJS whether to render js driven websites
	@return rows of strings. 1st row is the header and each of the rest rows
		is a comma separated string.
	"""
	assert name in ['英灵图鉴', '礼装图鉴'], "Cannot fetch csv data from %s" % name
	html_text = fetch_html_text(name, online, renderJS)

	reg = r'raw_str = "(.*)"'
	match = re.search(reg, html_text)
	rawstr = match.groups()[0]
	rows = rawstr.split('\\n')
	
	if not online:
		folder = os.path.join(CURDIR, '../../csv/')
		if not os.path.exists(folder):
			os.makedirs(folder)
		csvfile = os.path.join(folder, '%s.csv' % name)
		webfile = os.path.join(CURDIR, '../../web', '%s.html' % name)
		if not os.path.exists(csvfile) or \
			os.path.getmtime(csvfile) < os.path.getmtime(webfile):
			print('Updating %s ...' % os.path.relpath(csvfile))
			with codecs.open(csvfile, 'w', encoding='utf-8') as f:
				for row in rows:
					f.write('%s\n' % row)

	return rows

def fetch_all_cards_unrendered(urls, use_cache):
	"""
	This func does not support JS driven websites, since the js generated
	content is rendered in client only. Requests only get the original html.

	@param urls list of relative url after GAMECONF['url_webpage_root']
	@param use_cache whether to use cached html file on local disk
	"""
	for url in urls:
		if url in ['英灵图鉴', '礼装图鉴']:
			rows = fetch_csv_data(url, online=not use_cache, renderJS=False)
			yield rows
		elif use_cache:
			file = download_page(url, renderJS=False)

def fetch_all_cards_jsrendered(urls, use_cache):
	"""
	Utilize the new package: requests_html
	Ref: https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python
	Ref: https://github.com/psf/requests-html

	2020/9/18:
	Rendered html contains the scripts that fills in the web content!
	Gacha logic can refer to these scripts.

	@param urls list of relative url after GAMECONF['url_webpage_root']
	@param use_cache whether to use cached html file on local disk
	"""
	for url in urls:
		if url in ['英灵图鉴', '礼装图鉴']:
			rows = fetch_csv_data(url, online=not use_cache, renderJS=True)
		elif use_cache:
			file = download_page(url, renderJS=True)

def fetch_cards_summary(use_cache):
	urls = ['英灵图鉴', '礼装图鉴', '拉斯维加斯御前比试推荐召唤2/模拟器']
	fetch_all_cards_unrendered(urls, use_cache)
	# fetch_all_cards_jsrendered(urls, use_cache)

def write_html(html_text, filename):
	"""
	A helper function to better examin the heirarchy of a html tag.
	"""
	tmpfolder = os.path.join(CURDIR, '../../tmp')
	if not os.path.exists(tmpfolder):
		os.makedirs(tmpfolder)
	tagfile = os.path.join(tmpfolder, '%s.html' % filename)
	with codecs.open(tagfile, 'w') as f:
		soup = BeautifulSoup(html_text, 'html.parser')
		f.write(soup.prettify())

def fetch_servant_card_images(name_link, use_cache, renderJS=False):
	"""
	Fetch all of the images' link of the servant by name_link.
	
	@param online whether to fetch directly online without using cache
	@param renderJS whether to render js driven websites.
	@return list of image links in order of Phase 1, 2, 3, 4, costume,
			 and april fool
	"""
	s = datetime.now()
	html_text = fetch_html_text(name_link, \
		online=not use_cache, renderJS=renderJS)

	# BeautifulSoup is too slow and not user-tolerable whether using cache.
	# s = datetime.now()
	# soup = BeautifulSoup(html_text, 'html.parser')
	# graphpicker = soup.find(attrs={'class': 'graphpicker'})
	# e = datetime.now()
	# print('BeautifulSoup find the graphpicker costs: %s' % str(e - s))

	reg = r'(<div class="graphpicker".*</div>)<body>'
	graphpicker = re.search(reg, html_text).groups()[0]
	# write_html(graphpicker, filename='graphpicker')

	# If joinee path contains a leading '/', it is considered as absolute path,
	# any path before it will be discarded.
	reg = r'data-srcset=".*?1\.5x,\s/+(.*?)\s2x"'
	img_links = re.findall(reg, graphpicker)
	# with codecs.open(os.path.join(CURDIR, '../../tmp/img.txt'), 'w') as f:
	# 	for img_link in img_links:
	# 		f.write('%s\n' % img_link)

	e = datetime.now()
	print('Fetch servant_card_img (%s) costs: %s' % 
		('use cache' if use_cache else 'online', str(e - s)))

	img_root = GAMECONF['url_img_root']
	links = [os.path.join(img_root, link) for link in img_links]
	return links

def fetch_craft_card_images(name_link, use_cache, renderJS=False):
	"""
	Fetch all of the images' link of the servant by name_link.
	
	@param online whether to fetch directly online without using cache
	@param renderJS whether to render js driven websites.
	@return full-sized card image link
	"""
	s = datetime.utcnow()
	html_text = fetch_html_text(name_link, \
		online=not use_cache, renderJS=renderJS)

	reg = r'%s\.png.*?data-srcset=".*?1\.5x,\s/+(.*?)\s2x"' % name_link
	img_link = re.search(reg, html_text).groups()[0]

	e = datetime.utcnow()
	print('Fetch craft_card_img (%s) costs: %s' % 
		('use cache' if use_cache else 'online', str(e - s)))

	return os.path.join(GAMECONF['url_img_root'], img_link)

def main():
	use_cache = GAMECONF['use_cache']
	# fetch(use_cache)
	img_links = fetch_servant_card_images('玛修·基列莱特', use_cache)

	for link in img_links:
		img = cv2.imread(link)
		cv2.imshow('Card', img)
		cv2.waitKey(50)

if __name__ == '__main__':
	main()
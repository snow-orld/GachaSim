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
from datetime import date, datetime
import re

CURDIR = os.path.dirname(__file__)

def fetch_data(text, filename=None):
	'''
	Since all data is contained in the get_csv() function in the original html,
	the only left to do is to extract the raw string from the function.

	Returns
	-------
	- rows of strings. 1st row is the header and each of the rest rows
		is a comma separated string.
	'''
	reg = r'raw_str = "(.*)"'
	match = re.search(reg, text)
	rawStr = match.groups()[0]
	rows = rawStr.split('\\n')
	
	if filename:
		folder = os.path.join(CURDIR, '../../csv/')
		if not os.path.exists(folder):
			os.makedirs(folder)
		csvfile = os.path.join(folder, '%s.csv' % filename)
		webfile = os.path.join(CURDIR, '../../web', '%s.html' % filename)
		if not os.path.exists(csvfile) or \
			os.path.getmtime(csvfile) < os.path.getmtime(webfile):
			print('Updating %s ...' % os.path.relpath(csvfile))
			with codecs.open(csvfile, 'w', encoding='utf-8') as f:
				for row in rows:
					f.write('%s\n' % row)

	return rows

def fetch_unrendered(urls):
	'''
	This func does not support JS driven websites, since the js generated 
	content is rendered in client only. Requests only get the original html.
	'''
	# filenames = ['英灵图鉴', '礼装图鉴']
	filenames = urls
	
	for filename in filenames:
		filename = filename.replace('/', '-')
		url = os.path.join('https://fgo.wiki/w/', filename)
		webfile = os.path.join(CURDIR, '../../web', '%s.html' % filename)

		# This is added to prevent additional streams when testing.
		# Can be deleted during final depoloyment.
		if os.path.exists(webfile):
			print('%s already exists ...' % os.path.relpath(webfile))
			# Windows is internet access restricted
			if platform.system() == 'Windows':
				continue

		try:
			req = requests.get(url, stream=True)
		except requests.exceptions.ConnectionError:
			if not os.path.exists(webfile):
				print('Connection Failed. Please try again later to get %s.' \
					% os.path.basename(webfile))
			continue

		# Use the <li id="footer-info-lastmod"> tag to identify the 
		# last modified time
		try:
			reg = r'<li id="footer-info-lastmod">.*(\d{4})年(\d{1,2})月(\d{1,2})日' \
				r'\D*(\d{1,2}):(\d{1,2}).*</li>'
			y, m, d, H, M = [int(i) for i in re.search(reg, req.text).groups()]
			lastmod = '%i %i %i %i:%i:00 CST' % (d, m, y, H, M)
			lastmod = datetime.strptime(lastmod, '%d %m %Y %H:%M:%S %Z')
		except:
			lastmod = datetime.now()
		
		if not os.path.exists(webfile) or os.stat(webfile).st_size == 0 or \
			datetime.utcfromtimestamp(os.path.getmtime(webfile)) < lastmod:
			with codecs.open(webfile, 'w', encoding='utf-8') as f:
				print('Upating %s ...' % filename)
				f.write(req.text)

		if filename in ['英灵图鉴', '礼装图鉴']:
			with codecs.open(webfile, 'r', encoding='utf-8') as f:
				rows = fetch_data(f.read(), filename)

def fetch_jsrendered(urls):
	'''
	Utilize the new package: requests_html
	Ref: https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python
	Ref: https://github.com/psf/requests-html
	'''
	# names = ['英灵图鉴', '礼装图鉴']
	names = urls
	rooturl = 'https://fgo.wiki/w/'
	name = names[0]
	
	session = HTMLSession()
	r = session.get(os.path.join(rooturl, name))
	r.html.render()

	webfile = os.path.join(CURDIR, '../../web', '%s_rendered.html' % name)

	lastModified = datetime.strptime(r.headers['Last-Modified'], 
		'%a, %d %b %Y %H:%M:%S %Z')

	if not os.path.exists(webfile) or os.stat(webfile).st_size == 0 or \
		datetime.utcfromtimestamp(os.path.getmtime(webfile)) < lastModified:
		with codecs.open(webfile, 'w', encoding='utf-8') as f:
			print('Updating %s ...' % name)
			f.write(r.text)

def fetch():
	urls = ['英灵图鉴', '礼装图鉴', '拉斯维加斯御前比试推荐召唤2/模拟器']
	fetch_unrendered(urls)
	# fetch_jsrendered(urls)

def main():
	fetch()

if __name__ == '__main__':
	main()
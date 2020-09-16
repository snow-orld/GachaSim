#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file 		crawler.py
@author 	Xueman Mou
@created 	2020-9-15 17:00:00 GMT +0800
@version 	$Id: crawler.py 01 2020-9-15 17:00:00 GMT +0800 $
@env 		python 3.8.4

Fetch servant details from fgo.wiki.
TODO: fetch craft essence.

Ref: https://www.codementor.io/@codementorteam/how-to-scrape-an-ajax-website-using-python-qw8fuitvi
"""

import os, sys
import requests
import codecs
from requests_html import HTMLSession

CURDIR = os.path.dirname(__file__)

def fetch_legacy():
	'''
	This func does not support JS driven websites, since the js generated 
	content is rendered in client only. Requests only get the original html.

	@para servant fetch the servant page if set True, otherwise the craft page.
	'''
	filenames = ['英灵图鉴', '礼装图鉴']
	urls = ['%E8%8B%B1%E7%81%B5%E5%9B%BE%E9%89%B4', '%E7%A4%BC%E8%A3%85%E5%9B%BE%E9%89%B4']
	
	for filename in filenames:
		url = os.path.join('https://fgo.wiki/w/', filename)
		
		webfile = os.path.join('../../web', '%s.html' % filename)

		if os.path.exists(webfile):
			print('%s already exists ...' % webfile)
			continue

		try:
			response = requests.get(url, stream=True)
		except requests.exceptions.ConnectionError:
			print('Connection Failed. Please try again.')
			sys.exit(1)

		with codecs.open(webfile, 'w', encoding='utf-8') as f:
			print('Retriving %s ...' % filename) # Future work: animating with progress
			f.write(response.text)

def fetch():
	'''
	Utilize the new package: requests_html
	Ref: https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python
	Ref: https://github.com/psf/requests-html
	'''
	names = ['英灵图鉴', '礼装图鉴']
	rooturl = 'https://fgo.wiki/w/'
	name = names[0]
	
	session = HTMLSession()
	r = session.get(os.path.join(rooturl, name))
	r.html.render()

	webfile = os.path.join('../../web', '%s_rendered.html' % name)

	with codecs.open(webfile, 'w', encoding='utf-8') as f:
		print('Retriving %s ...' % name) # Future work: animating with progress
		f.write(r.text)

def main():
	fetch()

if __name__ == '__main__':
	main()
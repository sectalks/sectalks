#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#breakurl.py
#coding:utf8
import urllib
from bs4 import BeautifulSoup
from string import digits, ascii_uppercase, ascii_lowercase
import itertools
import multiprocessing
chars = digits + ascii_uppercase + ascii_lowercase
base = "http://base.url.here/secure.php?"
base = base+"ss=FQEPBRAcExcLHxMABhYSEBMFXUZEWAQAFUQNUwERR18DVUFNXVRdRRFbBAdCRAtWBREWCVEFSkFWH"
print base
def brute(c1):
	url = base+c1
	txt = urllib.urlopen(url).read()
	soup = BeautifulSoup(txt)
	try:
		res = soup.b.string.encode('utf-8', 'replace')
	except AttributeError:
		res = "null"
	if (res == "a"):
		print ('\n\nchar: '+res+'\n\nurl :'+url+'\n\n')
		f=open("breakurl-output", "a")
		f.write(res+'\n')
		f.write('\nurl: '+url)
		f.close()
for i in itertools.product(chars):
	brute(str(i[0]))

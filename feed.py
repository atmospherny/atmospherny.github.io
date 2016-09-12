#!/usr/bin/python

import urllib2
from urllib2 import urlopen, URLError, HTTPError
import xml.etree.ElementTree as ET
from datetime import date
import datetime
import os, sys

arxives = ["astro-ph", "nucl-ex", "nucl-th", "math-ph", "quant-ph", "cs"] #arxives to check
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def update():
	totalen = 0
	arr = ""
	arr2 = ""
	arr3 = ""
	print "Updating arXiv.org..."
	for j in arxives:
		sys.stdout.write("%s"%j)
		for k in range(20-len(j)): sys.stdout.write(".")
		txt = urllib2.urlopen("http://export.arxiv.org/rss/%s"%j)
		xml = ET.fromstring(txt.read())
		sys.stdout.write("%d\n"%len(list(xml)))
		totalen += len(list(xml))
		it = 0
		for child in xml:
			if it>1:
				arr += "%s{{{{ARTICLE_PARSER}}}}"%(child[0].text.split(" (arXiv:")[0].replace("\"","\\\""))			
				arr2 += "%s{{{{ARTICLE_PARSER}}}}"%(child[2].text.replace("\"","\\\""))
				arr3 += "%s{{{{ARTICLE_PARSER}}}}"%(child[1].text.replace("/abs/","/pdf/"))
			it+=1		
	with open("feed-template.html","r") as rf:
		inf = rf.read()
		inf = inf.replace(u"__ARXIV_TITLES__",arr)
		inf = inf.replace(u"__ARXIV_ABSTRACTS__",arr2)
		inf = inf.replace(u"__ARXIV_LINKS__",arr3)
		inf = inf.replace(u"__WEEKDAY__",days[datetime.date.weekday(datetime.date.today())])
		with open("feed.html","w") as outf:
			outf.write(inf.encode('utf-8'))

update()

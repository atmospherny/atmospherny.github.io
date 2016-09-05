#!/usr/bin/python

import urllib2
from urllib2 import urlopen, URLError, HTTPError
import xml.etree.ElementTree as ET
from datetime import date
import os, sys

arxives = ["astro-ph", "nucl-ex", "nucl-th", "math-ph", "quant-ph", "cs"] #arxives to check

def update():
	totalen = 0
	arr = ""
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
				arr += "<div><details><summary class='inner'><span class='arxiv-name'>%s&nbsp;&rarr;&nbsp;</span><a href='%s' target='_blank'>%s</a></summary>%s</details></div>"%(j,child[1].text.replace("/abs/","/pdf/"),child[0].text.split(" (arXiv:")[0],child[2].text)			
			it+=1
	with open("feed-template.html","r") as rf:
		inf = rf.read()
		inf = inf.replace("__ARXIV__",arr)
		with open("feed.html","w") as outf:
			outf.write(inf)
	print "====================%d"%totalen
	arr2 = ""
	print "Updating ISS reports..."
	txt = urllib2.urlopen("http://blogs.nasa.gov/stationreport/feed/")
	xml = ET.fromstring(txt.read())[0]
	for child in xml:
		if child.tag=="item":
			arr2 += "<div><details><summary class='inner'><a href='%s' target='_blank'>%s</a></summary><p>%s</p></details></div>"%(child[1].text,child[0].text,child[7].text)			
	with open("feed.html","r") as rf2:
		inf = unicode(rf2.read(),errors="ignore")
		inf = inf.replace("__ISSREP__",arr2)
		with open("feed.html","w") as outf2:
			outf2.write(inf.encode('utf-8'))
	arr2 = ""
	print "Updating NASA Breaking..."
	txt = urllib2.urlopen("https://www.nasa.gov/rss/dyn/breaking_news.rss")
	xml = ET.fromstring(txt.read())[0]
	for child in xml:
		if child.tag=="item":
			arr2 += "<div><details><summary class='inner'><a href='%s' target='_blank'>%s</a></summary><p>%s</p></details></div>"%(child[1].text,child[0].text,child[2].text)			
	with open("feed.html","r") as rf2:
		inf = unicode(rf2.read(),errors="ignore")
		inf = inf.replace("__NASABR__",arr2)
		with open("feed.html","w") as outf2:
			outf2.write(inf.encode('utf-8'))
	arr2 = ""
	print "Updating Science current..."
	txt = urllib2.urlopen("http://science.sciencemag.org/rss/current.xml")
	xml = ET.fromstring(txt.read())
	it = 0
	z = ""
	for child in xml:
		if it>0:
			for z1 in child:
				if z1.tag.split("}")[1]=="description":
					z = z1.text
					break
			arr2 += "<div><details><summary class='inner'><a href='%s' target='_blank'>%s</a></summary><p>%s</p></details></div>"%(child[1].text,child[0].text,z)			
		it+=1
	with open("feed.html","r") as rf2:
		inf = unicode(rf2.read(),errors="ignore")
		inf = inf.replace("__SCICUR__",arr2)
		with open("feed.html","w") as outf2:
			outf2.write(inf.encode('utf-8'))
	arr2 = ""
	print "Updating In-the-sky.org..."
	txt = urllib2.urlopen("https://in-the-sky.org//rss.php?feed=dfan&latitude=55.7522&longitude=37.6156&timezone=Europe/Moscow")
	xml = ET.fromstring(txt.read())[0]
	for child in xml:
		if child.tag=="item":
			arr2 += "<div><details><summary class='inner'><a href='%s' target='_blank'>%s</a></summary><p>%s</p></details></div>"%(child[1].text,child[0].text,child[2].text)			
	with open("feed.html","r") as rf2:
		inf = unicode(rf2.read(),errors="ignore")
		inf = inf.replace("__INTHESKY__",arr2)
		with open("feed.html","w") as outf2:
			outf2.write(inf.encode('utf-8'))
	arr2 = ""
	print "Updating n+1..."
	txt = urllib2.urlopen("https://nplus1.ru/rss")
	xml = ET.fromstring(txt.read())[0]
	for child in xml:
		if child.tag=="item":
			arr2 += "<div><details><summary class='inner'><span class='arxiv-name'>%s&nbsp;&rarr;&nbsp;</span><a href='%s' target='_blank'>%s</a></summary><p>%s</p></details></div>"%(child[6].text,child[4].text,child[0].text,child[1].text)			
	with open("feed.html","r") as rf2:
		inf = unicode(rf2.read(),errors="ignore")
		inf = inf.replace(u"__NPLUSONE__",arr2)
		with open("feed.html","w") as outf2:
			outf2.write(inf.encode('utf-8'))

update()
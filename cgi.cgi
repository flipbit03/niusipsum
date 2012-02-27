#!/usr/bin/python

__VERSION = "1.0"

print "content-type: text/plain; charset=utf-8\n"

## Issue Banner
print 'NIUSipsuM v%s by Cadu <cadu.coelho at gmail.com>' % (__VERSION)
print '------------------------'
print ''

# Make "feeds" folder also be in module path
import sys,os
subpaths = [ 'feeds' ]
for ___ in subpaths: sys.path.append(os.path.join(os.getcwd(),___))
del subpaths

# Additional modules
import random
from niusipsum import NiusIpsum

def r(n):
	return int(random.random()*n)


import f_folhaonline
import f_terra

print 'Lendo noticias...'
print ''
folhafeed = f_folhaonline.Feed('feed://feeds.folha.uol.com.br/emcimadahora/rss091.xml')
terrafeed = f_terra.Feed('feed://rss.terra.com.br/0,,EI1,00.xml')

datasources = [folhafeed, terrafeed]

mixer = []

for source in datasources:
	for entry in source.entries:
		title, data = entry
		mixer.append(data.strip())

print "Gerando poema....\n"

b = NiusIpsum(mixer, sectcount=4)
b.process()

print b.poem().encode('utf-8')


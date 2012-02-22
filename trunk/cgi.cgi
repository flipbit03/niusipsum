#!/usr/bin/python

__VERSION = "0.1"

print "content-type: text-plain; content-charset=utf-8\n"

## Issue Banner
print 'NIUSipsuM v%s' % (__VERSION)
print '------------------------'
print ''

# Make "feeds" folder also be in module path
import sys,os
subpaths = [ 'feeds' ]
for ___ in subpaths: sys.path.append(os.path.join(os.getcwd(),___))
del subpaths

# Additional modules
import random

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
		for line in data.split('.'):
			mixer.append(line.strip())

print 'Source: %d lines of juicy news' % (len(mixer))
print ''

howmanylines = max(20,r(40))
howmanylines = min(howmanylines, len(mixer))

print 'Will generate %d lines of newsy poetry...' % (howmanylines)


poem = []
for i in range(howmanylines):
	line = mixer[r(len(mixer))].strip()
	if line:
		poem.append(line)

text = '.\n'.join(poem)

print "\n---- LOUSY POETRY BEGIN ----\n"

print text.encode('utf-8')

print "\n---- LOUSY POETRY EOF ----"


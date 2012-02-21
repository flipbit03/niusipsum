import feedparser
import re

class BaseFeed():
	def __init__(self, url):
		self.url = url
		self.feedrawdata = []
		self.entries = []
		self.__update__()

	def __update__(self):
		self.feedrawdata = feedparser.parse(self.url)
		self.__process__()

	def __process__(self):
		self.entries = []
		for entry in self.feedrawdata['entries']:
			self.entries.append((entry.title, entry.description))


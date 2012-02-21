import feedparser
import re
from basefeed import BaseFeed

class Feed(BaseFeed):
	def __process__(self):
		for entry in self.feedrawdata['entries']:
			item = []
			item.append(entry.title)
			item.append(re.sub(r'&quot;','\"',re.sub(r'\n','',re.sub(r'\.\.\..?$','',re.sub(r'</?.+>','', entry.description)))).strip())
			
			self.entries.append(item)


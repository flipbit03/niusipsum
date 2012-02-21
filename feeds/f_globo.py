import feedparser
import re
from basefeed import BaseFeed

class Feed(BaseFeed):
	def __process__(self):
		for entry in self.feedrawdata['entries']:
			item = []
			item.append(entry.title)
			
			textdata = re.sub(r'\n','',re.sub(r'\.\.\..?$','',re.sub(r'</?.+>','', entry.description)))
			textdata = re.sub(r'\(.+\)\W?','',textdata) ### Remove stuff inside parenthesis
			textdata = textdata.replace('\n','') ### Remove newlines inside the code
			textdata = textdta.replace ('\t','')
			
			item.append(textdata.strip())
			self.entries.append(item)


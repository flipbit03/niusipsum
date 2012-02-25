#!/usr/bin/python
# -*- coding: cp1252 -*-
import re
import random
import sqlite3

data = open('sampledata/mixer.data.txt','rb').readlines()

class NiusIpsum:
# --------------- constructor

    def __init__(self, data, datacodec='utf-8', sectcount=4, sectlinecount=4, wordsperline=5, diversity=4):
        # store outside params
        self.data = []
        for line in data:
            self.data.append(line.decode(datacodec))
        self.sectcount = sectcount
        self.sectlinecount = sectlinecount
        self.wordsperline = wordsperline
        self.diversity = max(2, diversity) # affects how many rhyme components are used

        # we can now work
        self.isinit = True

        # storage for sentences
        self.pool = []
        self.rhymepool = {}

# --------------- randomization support

    def roll(self, sides, minimum=1):
		return max(minimum, int(random.random()*sides + 1) )

    def popnr(self, sourcelist, howmany=1):
		out = []
		src = sourcelist
		if howmany > len(sourcelist):
			raise Exception("NiusIpsum popnr(): HowMany > len(sourcelist) ???")
		else:
			for i in range(howmany):
				popped = src.pop(self.roll(len(src),minimum=0)-1)
				out.append(popped)
		return out

# --------------- text munging functions

    def process(self):
        if not self.isinit:
            raise Exception("NiusIpsum process(): isinit = False!")
        else:
            print "<NiusIpsum() Processing>"
            for line in self.data:
                print "#",
                sectionizedstring = self.sectionize(line, self.wordsperline)
                for ss in sectionizedstring:
                    rhyme = ss[-2:].lower()
                    self.pool.append( ( ss, self.sscore(ss), rhyme ) )
                    if not self.rhymepool.has_key(rhyme):
                        self.rhymepool[rhyme] = []
                        self.rhymepool[rhyme].append( (ss, self.sscore(ss)) )
                    else:
                        self.rhymepool[rhyme].append( (ss, self.sscore(ss)) )
                    print ".",

    def sectionize(self, t, wc=4):
        regexp = r'(?=(\b%s\w\w\w+))' % (r'\w+\s+'*(wc-1)) #notice the last word is at LEAST 3 chars \w\w\w+
        return re.findall(regexp, t, re.UNICODE)

    def sscore(self, t, wlen=3):
        score = 0;

        # Issue a number that is the number of chars in all words
        # in the sentence, given words > 3 characters

        # First, remove punctuation
        ts = re.sub(r'[\\\\\'\"\!\@\#\$\%\¨\&\*\(\)\_\-\=\+\´\`\[\]\{\}\^\~\,\.\;\:\/\?]',' ',t, re.UNICODE)

        # Then, strip trailing/leading space and split all words
        tswords = re.split(r'\s+', ts.strip(), re.UNICODE)

        # Now, iterate for every word and count with more than wlen letters
        for word in tswords:
            if len(word) > wlen:
                score = score + (len(word)-wlen)

        return score

# --------------- poem generation process
    
    def poem(self,a=10):
		totalscores = [ (x,y,g) for x in self.rhymepool.keys() for y in [sum([z[1] for z in self.rhymepool[x]])] for g in [len(self.rhymepool[x])] ]
		totalscores_sorted = sorted(totalscores, key = lambda sumscore: sumscore[1])[::-1]	# Sort by x[1] which is SCORE, and invert for DESCENDING with [::-1]
		return totalscores_sorted

	
    def generatepoemscript(self, sortedscorelist):
		# script
		thescript = []

		# how many rhymes per section
		rps = self.sectlinecount // 4

		# how many single sentences per section
		sss = self.sectlinecount % 4
		
		# how many rhymes (read, 4 intertwined sentences) do we need?
		totalrc = (rps) * self.sectcount

		#adjust diversity
		adjdivers = min(self.roll(self.diversity, minimum=2), len(sortedscorelist))

		#get elements using adjusted diversity as a cutoff
		try:
			elements = [x[0] for x in sortedscorelist[0:adjdivers]]
		except:
			raise Exception("NiusIpsum generatepoemscript(): adjdivers > len(scorelist)")

		for section in range(self.sectcount):
			#SECTION
			pass

		return elements









b = NiusIpsum(data)
b.process()

z = b.poem()

exi = b.generatepoemscript(z)

print 'exi --> ' + repr(exi)

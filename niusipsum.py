#!/usr/bin/python
# -*- coding: cp1252 -*-
import re
import random
import sqlite3

data = open('sampledata/mixer.data.txt','rb').readlines()

class NiusIpsum:
    def __init__(self, data, datacodec='utf-8', sectcount=4, sectlinecount=4, wordsperline=5):
        # store outside params
        self.data = []
        for line in data:
            self.data.append(line.decode(datacodec))
        self.sectcount = sectcount
        self.sectlinecount = sectlinecount
        self.wordsperline = wordsperline

        # we can now work
        self.isinit =  True

        # storage for sentences
        self.pool = []
        self.rhymepool = {}

    def process(self):
        if not self.isinit:
            raise Exception("NiusIpsum isinit = False!")
        else:
            print "<NiusIpsum() Processing>"
            for line in self.data:
                print "#",
                sectionizedstring = self.sectionize(line, self.wordsperline)
                for ss in sectionizedstring:
                    rhyme = ss[-2:]
                    self.pool.append( ( ss, self.sscore(ss), rhyme ) )
                    if not self.rhymepool.has_key(rhyme):
                        self.rhymepool[rhyme] = []
                        self.rhymepool[rhyme].append( (ss, self.sscore(ss)) )
                    else:
                        self.rhymepool[rhyme].append( (ss, self.sscore(ss)) )
                    print ".",

    def sectionize(self, t, wc=4):
        regexp = r'(?=(\b%s\w\w\w\w+))' % (r'\w+\s+'*(wc-1))
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

b = NiusIpsum(data)
b.process()

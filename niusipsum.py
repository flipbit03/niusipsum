#!/usr/bin/python
# -*- coding: cp1252 -*-
import re
import random

class NiusIpsum:
# --------------- constructor
    def __init__(self, data, datacodec='utf-8', sectcount=4, sectlinecount=4, wordsperline=5, diversity=4, debug=False):
        # store outside params
        self.data = []
        for line in data:
            if isinstance(line, unicode):
                self.data.append(line)
            elif isinstance(line, str):
                self.data.append(line.decode(datacodec))

        self.sectcount = sectcount
        self.sectlinecount = sectlinecount
        self.wordsperline = wordsperline
        self.diversity = max(2, diversity) # affects how many rhyme components are used

		# debug?
        self.debug = debug

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
            for line in self.data:
                sectionizedstring = self.sectionize(line, self.wordsperline)
                for ss in sectionizedstring:
                    rhyme = ss[-2:].lower()
                    self.pool.append( ( ss, self.sscore(ss), rhyme ) )
                    if not self.rhymepool.has_key(rhyme):
                        self.rhymepool[rhyme] = []
                        self.rhymepool[rhyme].append( (ss, self.sscore(ss)) )
                    else:
                        self.rhymepool[rhyme].append( (ss, self.sscore(ss)) )

    def sectionize(self, t, wc=4):
        regexp = r'(?=(\b%s\w\w\w\w\w\w\w+))' % (r'\w+\s+'*(wc-1)) #notice the last word is at LEAST 7 chars \w\w\w\w\w+
        return re.findall(regexp, t, re.UNICODE)

    def sscore(self, t, wlen=3):
        score = 0;

        # Issue a number that is the number of chars in all words
        # in the sentence, given words > 3 characters

        # First, remove punctuation
        ts = re.sub(r'[\\\\\'\"\!\@\#\$\%\�\&\*\(\)\_\-\=\+\�\`\[\]\{\}\^\~\,\.\;\:\/\?]',' ',t, re.UNICODE)

        # Then, strip trailing/leading space and split all words
        tswords = re.split(r'\s+', ts.strip(), re.UNICODE)

        # Now, iterate for every word and count with more than wlen letters
        for word in tswords:
            if len(word) > wlen:
                score = score + (len(word)-wlen)

        return score

# --------------- poem generation process

        # --------------- poem elements

    def _elm_rhyme(self, elements):
        belem = []

        out = []

        a, b = self.popnr(elements,2)

        if (self.roll(2)-1): # either A,B or B,A
            belem.append(a)
            belem.append(a)
            belem.append(b)
            belem.append(b)

        else:
            belem.append(b)
            belem.append(b)
            belem.append(a)
            belem.append(a)

        out += belem

        return out

    def _elm_sentence(self, elements, howmany=1):
        out = []

        for i in range(howmany):
            a = self.popnr(elements,1)
            out += a

        return out

        # --------------- poem generation logic

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

        if self.debug:
            print "Debug:POEM[",
        for section in range(self.sectcount):
            if self.debug:
                print "sec/",
            # Add rhymes
            for rhymes in range(rps):
                if self.debug:
                    print "rhyme ",
                thescript += self._elm_rhyme(elements[:])

            # Add single sentences, filling the section
            for sentences in range(sss):
                if self.debug:
                    print "single ",
                thescript += self._elm_sentence(elements[:])

            # Add blank space, meaning section separator
            thescript.append('')
        if self.debug:
            print "]\n"

        return thescript


    def poem(self):
        out = []

        # Get a list containting | x->rhymekey name | y->total score | z->amount of sentences
        totalscores = [ (x,y,g) for x in self.rhymepool.keys() for y in [sum([z[1] for z in self.rhymepool[x]])] for g in [len(self.rhymepool[x])] ]
        # Sort by x[1] which is SCORE, and invert for DESCENDING with [::-1]
        totalscores_sorted = sorted(totalscores, key = lambda sumscore: sumscore[1])[::-1]

        # With the total sorted scores, generate the poem script.
        poemscript = self.generatepoemscript(totalscores_sorted)

        for line in poemscript:
            if not line:
                out.append(' ') # Append blank link when asked to, with a false-evaluated string ''
            else:
                if self.debug: 
                    print "Len rhymepool[%s] = %d" % (line, len(self.rhymepool[line])),
                out.append(self.popnr(self.rhymepool[line])[0][0])
                if self.debug: 
                    print " => %d" % (len(self.rhymepool[line]))

        return '\n'.join(out)

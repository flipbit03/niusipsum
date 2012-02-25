#!/usr/bin/python
# -*- coding: cp1252 -*-
import re
import random
import sqlite3
from niusipsum import NiusIpsum

data = open('sampledata/mixer.data.txt','rb').readlines()

b = NiusIpsum(data, sectlinecount=4)
b.process()

print b.poem()

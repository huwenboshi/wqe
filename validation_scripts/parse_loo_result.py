#!/usr/bin/python

from optparse import OptionParser
import sys
import math
import time

# get command line
parser = OptionParser()
parser.add_option("-l", "--loofile", dest="loofile")
parser.add_option("-o", "--outfile", dest="outfile")
(options, args) = parser.parse_args()
loofile_nm = options.loofile
outfile_nm = options.outfile

# check command line
if(loofile_nm == None or outfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -l to specify loofile\n")
    sys.stderr.write("\tUse -o to specify outfile\n")
    sys.exit()


# result
ncorrect = 0
ntotal = 0

loofile = open(loofile_nm, 'r')
for line in loofile:
    line = line.strip()
    cols = line.split('\t')
    cnts = cols[2].split(',')
    if(len(cols) < 5):
        continue
    for i in xrange(4,len(cols)):
        results = cols[i].split(',')
        tp = results[0].split('/')
        truth = tp[0]
        pred = tp[1]
        score = float(results[1])
        if(score > 0.95):
            ntotal += 1.0
            if(truth == pred):
                ncorrect += 1.0
loofile.close()

print '%f/%f=%f' % (ncorrect,ntotal,ncorrect/ntotal)

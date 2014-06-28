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
    ncps = 0.0
    ntps = 0.0
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
        if(score > 0.83):
            ntotal += 1.0
            ntps += 1.0
            if(truth == pred):
                ncorrect += 1.0
                ncps += 1.0
    if(ntps != 0):
        accps = ncps/ntps
        if(accps < 1.0):
            line = cols[0]+'\t'+cols[1]+'\t'+str(ncps/ntps)
            print line
loofile.close()

print '%f/%f=%f' % (ncorrect,ntotal,ncorrect/ntotal)

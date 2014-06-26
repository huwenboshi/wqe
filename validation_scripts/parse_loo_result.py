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
    print cols[3]


loofile.close()

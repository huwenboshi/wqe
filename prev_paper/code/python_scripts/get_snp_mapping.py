#!/usr/bin/python

import sys
import math
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-c", "--csvfile", dest="csvfile")

(options, args) = parser.parse_args()

csvfile_nm = options.csvfile

if(csvfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -c to specify csv file\n")
    sys.exit()

csvfile = open(csvfile_nm, 'r')
for line in csvfile:
    line = line.strip()
    if(line[0] == '#'):
        continue
    cols = line.split(',')
    affysnp = cols[0].replace('"','')
    rssnp = cols[1].replace('"','')
    snpa = cols[8].replace('"','')
    snpb = cols[9].replace('"','')
    print affysnp+'\t'+rssnp+'\t'+snpa+'\t'+snpb
csvfile.close()

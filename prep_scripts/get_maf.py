#!/usr/bin/python

import sys
import math
from optparse import OptionParser
from random import shuffle

parser = OptionParser()
parser.add_option("-s", "--snpfile", dest="snpfile")
parser.add_option("-m", "--mapfile", dest="mapfile")

(options, args) = parser.parse_args()

snpfile_nm = options.snpfile
mapfile_nm = options.mapfile

if(snpfile_nm == None or mapfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -s to specify snpfile\n")
    sys.stderr.write("\tUse -m to specify mapfile\n")
    sys.exit()

snp_maf = dict()
mapfile = open(mapfile_nm, 'r')
flr = False
for line in mapfile:
    if(flr == False):
        flr = True
        continue
    line = line.strip()
    cols = line.split()
    snpid = cols[0]
    freq = float(cols[2])
    if(freq > 0.5):
        freq = 1.0-0.5
    snp_maf[snpid] = freq
mapfile.close()

snpfile = open(snpfile_nm, 'r')
for line in snpfile:
    line = line.strip()
    print line, snp_maf[line]
snpfile.close()

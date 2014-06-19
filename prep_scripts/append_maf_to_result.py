#!/usr/bin/python

import sys
import math
from optparse import OptionParser
from random import shuffle

parser = OptionParser()
parser.add_option("-r", "--resultfile", dest="resultfile")
parser.add_option("-m", "--maffile", dest="maffile")

(options, args) = parser.parse_args()

resultfile_nm = options.resultfile
maffile_nm = options.maffile

if(resultfile_nm == None or maffile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -r to specify resultfile\n")
    sys.stderr.write("\tUse -m to specify maffile\n")
    sys.exit()

snp_maf = dict()
maffile = open(maffile_nm,'r')
for line in maffile:
    line = line.strip()
    cols = line.split()
    snp = cols[0]
    maf = cols[1]
    snp_maf[snp] = maf
maffile.close()

resultfile = open(resultfile_nm,'r')
for line in resultfile:
    line = line.strip()
    cols = line.split()
    snp = cols[0]
    result = cols[1]
    print snp_maf[snp], result
resultfile.close()

#!/usr/bin/python

import sys
import math
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-a", "--afile", dest="afile")
parser.add_option("-b", "--bfile", dest="bfile")

(options, args) = parser.parse_args()

afile_nm = options.afile
bfile_nm = options.bfile

if(afile_nm == None or bfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -a to specify afile\n")
    sys.stderr.write("\tUse -b to specify bfile\n")
    sys.exit()

flr = False
afile = open(afile_nm, 'r')
afile_indvs = []
snp_indv_int_a = dict()
snps_a = []
for line in afile:
    line = line.strip()
    if(flr == False):
        flr = True
        cols = line.split()
        for i in xrange(1,len(cols)):
            indv = cols[i].split('_')[1]
            afile_indvs.append(indv)
        continue
    cols = line.split()
    snp = cols[0].replace('"', '')
    snps_a.append(snp)
    snp_indv_int_a[snp] = []
    for i in xrange(1, len(cols)):
        snp_indv_int_a[snp].append(cols[i])
afile.close()

flr = False
bfile = open(bfile_nm, 'r')
bfile_indvs = []
snps_b = []
snp_indv_int_b = dict()
for line in bfile:
    line = line.strip()
    if(flr == False):
        flr = True
        cols = line.split()
        for i in xrange(1,len(cols)):
            indv = cols[i].split('_')[1]
            bfile_indvs.append(indv)
        continue
    cols = line.split()
    snp = cols[0].replace('"', '')
    snps_b.append(snp)
    snp_indv_int_b[snp] = []
    for i in xrange(1, len(cols)):
        snp_indv_int_b[snp].append(cols[i])
bfile.close()

first_line = ''
for indv in afile_indvs:
    first_line += indv + '\t'
print first_line

for snp in snps_a:
    line = snp + '\t'
    indv_int_a = snp_indv_int_a[snp]
    indv_int_b = snp_indv_int_b[snp]
    for i in xrange(len(afile_indvs)):
        line += indv_int_a[i] + '/' + indv_int_b[i]
        line += '\t'
    print line

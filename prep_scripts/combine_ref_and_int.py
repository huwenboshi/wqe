#!/usr/bin/python

import sys
import math
from optparse import OptionParser
from random import shuffle

parser = OptionParser()
parser.add_option("-r", "--reffile", dest="reffile")
parser.add_option("-i", "--intfile", dest="intfile")
parser.add_option("-m", "--mapfile", dest="mapfile")

(options, args) = parser.parse_args()

reffile_nm = options.reffile
intfile_nm = options.intfile
mapfile_nm = options.mapfile

if(intfile_nm == None or reffile_nm == None or mapfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -r to specify reffile\n")
    sys.stderr.write("\tUse -i to specify intfile\n")
    sys.stderr.write("\tUse -m to specify mapfile\n")
    sys.exit()

# get allele mapping
snp_allele = dict()
mapfile = open(mapfile_nm, 'r')
for line in mapfile:
    line = line.strip()
    cols = line.split()
    snp = cols[0]
    allele = cols[2]+'/'+cols[3]
    snp_allele[snp] = allele
mapfile.close()

# get snp information
snp_info = dict()
snp_ind_geno = dict()
reffile = open(reffile_nm, 'r')
indv_list = []
flr = False
for line in reffile:
    line = line.strip()
    cols = line.split()
    if(flr == False):
        flr = True
        indv_list = cols
        continue
    snp = cols[0]
    freq = cols[2]
    snp_info[snp] = (snp_allele[snp],freq)
    snp_ind_geno[snp] = dict()
    for i in xrange(3,len(cols)):
        snp_ind_geno[snp][indv_list[i-3]] = cols[i]
reffile.close()

# get intensity
intfile = open(intfile_nm, 'r')
indv_list = []
shuffled_indv_list = []
flr = False
for line in intfile:
    line = line.strip()
    cols = line.split()
    if(flr == False):
        flr = True
        indv_list = cols
        shuffled_indv_list = indv_list[:]
        shuffle(shuffled_indv_list)
        print '\t'.join(shuffled_indv_list)
        continue
    snp = cols[0]
    if(snp not in snp_ind_geno):
        continue
    ind_int = dict()
    for i in xrange(1, len(cols)):
        ind_int[indv_list[i-1]] = cols[i]
    info = snp_info[snp]
    ind_geno = snp_ind_geno[snp]
    out = snp+'\t'+info[0]+'\t'+info[1]+'\t'
    for ind in shuffled_indv_list:
        out += ind_int[ind]+':'+ind_geno[ind]+'\t'
    print out
intfile.close()

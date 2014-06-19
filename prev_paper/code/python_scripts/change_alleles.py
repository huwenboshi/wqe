#!/usr/bin/python

import sys
import math
from optparse import OptionParser
from random import shuffle

def comp(c):
    if(c == 'A'):
        return 'T'
    if(c == 'T'):
        return 'A'
    if(c == 'C'):
        return 'G'
    if(c == 'G'):
        return 'C'

def fix_encoding(affy, hap):
    if((affy[0] == hap[0] and affy[1] == hap[1]) or
       (affy[1] == hap[0] and affy[0] == hap[1])):
        return {hap[0]: hap[0], hap[1]:hap[1]}
    elif((comp(hap[0]) == affy[0] and hap[1] == affy[1]) or
         (comp(hap[0]) == affy[1] and hap[1] == affy[0])):
        return {hap[0]: comp(hap[0]), hap[1]:hap[1]}
    elif((comp(hap[1]) == affy[0] and hap[0] == affy[1]) or
         (comp(hap[1]) == affy[1] and hap[0] == affy[0])):
        return {hap[0]: hap[0], hap[1]:comp(hap[1])}
    else:
        return {hap[0]: comp(hap[0]), hap[1]: comp(hap[1])}

parser = OptionParser()
parser.add_option("-a", "--hapmart", dest="hapmart")
parser.add_option("-m", "--mapfile", dest="mapfile")

(options, args) = parser.parse_args()

hapmart_nm = options.hapmart
mapfile_nm = options.mapfile

if(hapmart_nm == None or mapfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -a to specify hapmart\n")
    sys.stderr.write("\tUse -m to specify mapfile\n")
    sys.exit()

mapfile = open(mapfile_nm, 'r')
snp_allele = dict()
for line in mapfile:
    line = line.strip()
    cols = line.split()
    affysnp = cols[0]
    allele = (cols[2],cols[3])
    snp_allele[affysnp] = allele
mapfile.close()

hapmart = open(hapmart_nm, 'r')
indv_list = []
flr = False
for line in hapmart:
    line = line.strip()
    cols = line.split()
    if(flr == False):
        flr = True
        indv_list = cols
        print '\t'.join(indv_list)
        continue
    snp = cols[0]
    hap_allele = tuple(cols[1].split('/'))
    freq = cols[2]
    affy_allele = snp_allele[snp]
    encode = fix_encoding(affy_allele, hap_allele)
    new_hap_allele = (encode[hap_allele[0]], encode[hap_allele[1]])
    out = snp+'\t'+new_hap_allele[0]+'/'+new_hap_allele[1]+'\t'+freq+'\t'
    for i in xrange(3, len(cols)):
        if(cols[i] == 'NN'):
            out += cols[i]
        else:
            out += encode[cols[i][0]]+encode[cols[i][1]]
        out += '\t'
    print out
hapmart.close()

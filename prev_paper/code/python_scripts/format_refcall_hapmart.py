#!/usr/bin/python

import sys
import math
from optparse import OptionParser
from random import shuffle

parser = OptionParser()
parser.add_option("-a", "--hapmart", dest="hapmart")
parser.add_option("-i", "--indvfile", dest="indvfile")
parser.add_option("-m", "--mapfile", dest="mapfile")

(options, args) = parser.parse_args()

hapmart_nm = options.hapmart
indvfile_nm = options.indvfile
mapfile_nm = options.mapfile

if(hapmart_nm == None or indvfile_nm == None or mapfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -a to specify hapmart\n")
    sys.stderr.write("\tUse -i to specify indvfile\n")
    sys.stderr.write("\tUse -m to specify mapfile\n")
    sys.exit()

indv_list = []
indv_set = set()
indvfile = open(indvfile_nm, 'r')
for line in indvfile:
    line = line.strip()
    indv_set.add(line)
    indv_list.append(line)
indvfile.close()
shuffle(indv_list)

snp_map = dict()
mapfile = open(mapfile_nm, 'r')
for line in mapfile:
    line = line.strip()
    cols = line.split()
    snp_map[cols[1]] = cols[0]
mapfile.close()

flr = False
hapmart = open(hapmart_nm, 'r')
snp_sample_geno = dict()
snp_info = dict()
for line in hapmart:
    line = line.strip()
    if(flr == False):
        flr = True
        continue
    cols = line.split('\t')
    rsid = cols[1]
    if(rsid not in snp_map):
        continue
    affyid = snp_map[rsid]
    alleles = cols[0]
    freq = cols[5]
    snp_info[affyid] = (alleles, freq)
    samples = cols[2].split()
    genos = cols[3].split()
    sample_geno = dict()
    for i in xrange(len(genos)):
        if((samples[i] in sample_geno and sample_geno[samples[i]] == 'NN') or
           (samples[i] not in sample_geno)):
            sample_geno[samples[i]] = genos[i]
    snp_sample_geno[affyid] = sample_geno
hapmart.close()

print '\t'.join(indv_list)

for snp in snp_sample_geno:
    sample_geno = snp_sample_geno[snp]
    info = snp_info[snp]
    out = snp+'\t'+info[0]+'\t'+info[1]+'\t'
    for ind in indv_list:
        if(ind in sample_geno):
            out += sample_geno[ind]
        else:
            out += 'NN'
        out += '\t'
    print out 

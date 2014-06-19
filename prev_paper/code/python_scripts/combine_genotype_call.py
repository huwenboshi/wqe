#!/usr/bin/python

import sys
import math
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", "--dir", dest="dir")
parser.add_option("-f", "--files", dest="files")

(options, args) = parser.parse_args()

dir_nm = options.dir
files_nm = options.files

if(dir_nm == None or files_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -d to specify dir\n")
    sys.stderr.write("\tUse -f to specify files\n")
    sys.exit()

indv_set = set()
snp_allele = dict()
snp_indv_geno = dict()
files = open(files_nm, 'r')
for line in files:
    line = line.strip()
    path = dir_nm + line
    sys.stderr.write(path+'\n')
    f = open(path, 'r')
    indvs = []
    flr = False
    for l in f:
        l = l.strip()
        cols = l.split()
        if(flr == False):
            flr = True
            for i in xrange(11,len(cols)):
                indvs.append(cols[i])
                indv_set.add(cols[i])
            continue
        snp = cols[0]
        allele = cols[1]
        snp_allele[snp] = allele
        snp_indv_geno[snp] = dict()
        for i in xrange(len(indvs)):
            snp_indv_geno[snp][indvs[i]] = cols[i+11]
    f.close()
files.close()

indv_list = list(indv_set)
line = ''
for indv in indv_list:
    line += indv+'\t'
print line

for snp in snp_indv_geno:
    line = snp + '\t' + snp_allele[snp] + '\t'
    indv_geno = snp_indv_geno[snp]
    for indv in indv_list:
        if(indv in indv_geno):
            line += indv_geno[indv] + '\t'
        else:
            line += 'NN\t'
    print line

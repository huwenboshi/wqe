#!/usr/bin/python

from optparse import OptionParser
import sys
import math
import time

# get command line
parser = OptionParser()
parser.add_option("-f", "--fullfile", dest="fullfile")
parser.add_option("-n", "--nparts", dest="nparts")
(options, args) = parser.parse_args()
fullfile_nm = options.fullfile
nparts_str = options.nparts

# check command line
if(fullfile_nm == None or nparts_str == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -f to specify fullfile\n")
    sys.stderr.write("\tUse -n to specify nparts\n")
    sys.exit()

# files for saving the result
nparts = int(nparts_str)

# read in data
snp_indv_geno = dict()
indv_list = []
fullfile = open(fullfile_nm, 'r')
flr = False
snp_list = []
for line in fullfile:

    # get line
    line = line.strip()
    cols = line.split()
    
    # get individuals
    if(flr == False):
        flr = True
        indv_list = cols
        continue
    indv_geno = dict()

    # get snp id
    snp = cols[0]
    snp_list.append(snp)

    # get snp information - alleles and frequency
    alleles = cols[1]
    sensea = cols[1][0]
    senseb = cols[1][2]
    freq = cols[2]
    
    # parse out genotype information
    for i in xrange(len(indv_list)):
        indv_geno[indv_list[i]] = cols[i+3]
    
    # add to collection
    snp_indv_geno[snp] = (freq, alleles, indv_geno)

# do the partition
nspp = int(math.floor(len(snp_indv_geno)/nparts))
for i in xrange(nparts):
    print i
    outfile = open(fullfile_nm+'.'+str(i),'w')
    outline = '\t'.join(indv_list)+'\n'
    outfile.write(outline)
    st = i*nspp
    ed = st+nspp
    if(i == nparts-1):
        ed = len(snp_list)
    snpinp = snp_list[st:ed]
    
    for s in snpinp:
        outline = ''
        fai = snp_indv_geno[s]
        alleles = fai[1]
        freq = fai[0]
        indv_geno = fai[2]
        outline += s+'\t'+str(alleles)+'\t'+str(freq)+'\t'
        
        for indv in indv_list:
            outline += indv_geno[indv]+'\t'
        outfile.write(outline+'\n')
        
    outfile.close()

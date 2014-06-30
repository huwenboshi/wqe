#!/usr/bin/python

from optparse import OptionParser
import sys
import math
import time

# get command line
parser = OptionParser()
parser.add_option("-r", "--crlmm", dest="crlmmfile")
parser.add_option("-c", "--socal", dest="socalfile")
parser.add_option("-s", "--snps", dest="snpsfile")

(options, args) = parser.parse_args()

crlmmfile_nm = options.crlmmfile
socalfile_nm = options.socalfile
snpsfile_nm = options.snpsfile

# check command line
if(crlmmfile_nm == None or socalfile_nm == None or snpsfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -r to specify crlmmfile\n")
    sys.stderr.write("\tUse -c to specify socalfile\n")
    sys.stderr.write("\tUse -s to specify snpsfile\n")
    sys.exit()

# read in snps of interest
snps_set = set()
snpsfile = open(snpsfile_nm, 'r')
for line in snpsfile:
    line = line.strip()
    snps_set.add(line)
snpsfile.close()

# read in socal file
socal_snp_indv_geno = dict()
socalfile = open(socalfile_nm, 'r')
flr = False
socal_indv_list = []
for line in socalfile:
    line = line.strip()
    if(flr == False):
        socal_indv_list = line.split()
        flr = True
        continue

    cols = line.split()
    snpid = cols[0]

    # skip snps not of interest
    if(snpid not in snps_set):
        continue
    
    # read in genotypes
    socal_snp_indv_geno[snpid] = dict()
    for i in xrange(len(socal_indv_list)):
        genotype = cols[i+1]
        socal_snp_indv_geno[snpid][socal_indv_list[i]] = genotype
socalfile.close()

# compare with crlmm
naaaa = 0.0
naaab = 0.0
naabb = 0.0

nabaa = 0.0
nabab = 0.0
nabbb = 0.0

nbbaa = 0.0
nbbab = 0.0
nbbbb = 0.0

ntot = 0.0
ncorrect = 0.0

crlmmfile = open(crlmmfile_nm, 'r')
flr = False
crlmm_indv_list = []
for line in crlmmfile:
    line = line.strip()
    if(flr == False):
        crlmm_indv_list = line.split()
        for i in xrange(len(crlmm_indv_list)):
            tmp = crlmm_indv_list[i].split('_')[1]
            crlmm_indv_list[i] = tmp
        flr = True
        continue

    cols = line.split()
    snpid = cols[0]

    if(snpid not in snps_set):
        continue
    
    # read individual genotype
    crlmm_indv_geno = dict()
    for i in xrange(len(crlmm_indv_list)):
        genotype = cols[i+1]
        if(genotype == '1'):
            genotype = 'aa'
        elif(genotype == '2'):
            genotype = 'ab'
        elif(genotype == '3'):
            genotype = 'bb'
        crlmm_indv_geno[crlmm_indv_list[i]] = genotype
    
    # compare with socal
    socal_indv_geno = socal_snp_indv_geno[snpid]
    for indv in socal_indv_geno:
        if(indv not in crlmm_indv_geno):
            continue
        socal_call = socal_indv_geno[indv]
        crlmm_call = crlmm_indv_geno[indv]
        
        if(crlmm_call == 'aa' and socal_call == 'aa'):
            naaaa += 1.0
        elif(crlmm_call == 'aa' and socal_call == 'ab'):
            naaab += 1.0
        elif(crlmm_call == 'aa' and socal_call == 'bb'):
            naabb += 1.0
        
        elif(crlmm_call == 'ab' and socal_call == 'aa'):
            nabaa += 1.0
        elif(crlmm_call == 'ab' and socal_call == 'ab'):
            nabab += 1.0
        elif(crlmm_call == 'ab' and socal_call == 'bb'):
            nabbb += 1.0
        
        elif(crlmm_call == 'bb' and socal_call == 'aa'):
            nbbaa += 1.0
        elif(crlmm_call == 'bb' and socal_call == 'ab'):
            nbbab += 1.0
        elif(crlmm_call == 'bb' and socal_call == 'bb'):
            nbbbb += 1.0
crlmmfile.close()



print 'CRLMM\SoCal\tAA\tAB\tBB'
print 'AA\t\t%d\t%d\t%d' % (naaaa, naaab, naabb)
print 'AB\t\t%d\t%d\t%d' % (nabaa, nabab, nabbb)
print 'BB\t\t%d\t%d\t%d' % (nbbaa, nbbab, nbbbb)

tot1 = naaaa+naaab+naabb
tot2 = nabaa+nabab+nabbb
tot3 = nbbaa+nbbab+nbbbb
overallacc = (naaaa+nabab+nbbbb)/(tot1+tot2+tot3)
print overallacc

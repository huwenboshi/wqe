#!/usr/bin/python

from optparse import OptionParser
import sys
import math
import time

# get command line
parser = OptionParser()
parser.add_option("-a", "--hapmart", dest="hapmartfile")
parser.add_option("-c", "--crlmm", dest="crlmmfile")
parser.add_option("-s", "--snps", dest="snpsfile")
parser.add_option("-m", "--map", dest="mapfile")

(options, args) = parser.parse_args()

hapmartfile_nm = options.hapmartfile
crlmmfile_nm = options.crlmmfile
snpsfile_nm = options.snpsfile
mapfile_nm = options.mapfile

# check command line
if(hapmartfile_nm == None or crlmmfile_nm == None or
   snpsfile_nm == None or mapfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -a to specify hapmartfile\n")
    sys.stderr.write("\tUse -c to specify crlmmfile\n")
    sys.stderr.write("\tUse -s to specify snpsfile\n")
    sys.stderr.write("\tUse -m to specify mapfile\n")
    sys.exit()

# read in map file
snp_map = dict()
mapfile = open(mapfile_nm, 'r')
for line in mapfile:
    line = line.strip()
    cols = line.split()
    snpid = cols[0]
    allele_a = cols[2]
    allele_b = cols[3]
    snp_map[snpid] = (allele_a,allele_b)
mapfile.close()

# read in snps of interest
snps_set = set()
snpsfile = open(snpsfile_nm, 'r')
for line in snpsfile:
    line = line.strip()
    snps_set.add(line)
snpsfile.close()

# read in crlmm file
crlmm_snp_indv_geno = dict()
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

    # skip snps not of interest
    if(snpid not in snps_set):
        continue
    
    # read in genotypes
    crlmm_snp_indv_geno[snpid] = dict()
    for i in xrange(len(crlmm_indv_list)):
        genotype = cols[i+1]
        if(genotype == '1'):
            genotype = 'aa'
        elif(genotype == '2'):
            genotype = 'ab'
        elif(genotype == '3'):
            genotype = 'bb'
        crlmm_snp_indv_geno[snpid][crlmm_indv_list[i]] = genotype
crlmmfile.close()

# compare with hapmart
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

hapmartfile = open(hapmartfile_nm, 'r')
flr = False
hapmart_indv_list = []
for line in hapmartfile:
    line = line.strip()
    if(flr == False):
        hapmart_indv_list = line.split()
        flr = True
        continue
    cols = line.split()
    snpid = cols[0]
    alleles = snp_map[snpid]
    a = alleles[0]
    b = alleles[1]
    
    if(snpid not in snps_set):
        continue
    
    # read individual genotype
    hapmart_indv_geno = dict()
    for i in xrange(len(hapmart_indv_list)):
        genotype = cols[i+3]
        if(genotype == 'NN'):
            continue
        if(genotype == a+a):
            genotype = 'aa'
        elif(genotype == a+b or genotype == b+a):
            genotype = 'ab'
        elif(genotype == b+b):
            genotype = 'bb'
        hapmart_indv_geno[hapmart_indv_list[i]] = genotype
    
    # compare with crlmm
    crlmm_indv_geno = crlmm_snp_indv_geno[snpid]
    for indv in crlmm_indv_geno:
        if(indv not in hapmart_indv_geno):
            continue
        crlmm_call = crlmm_indv_geno[indv]
        hapmart_call = hapmart_indv_geno[indv]
        
        if(hapmart_call == 'aa' and crlmm_call == 'aa'):
            naaaa += 1.0
        elif(hapmart_call == 'aa' and crlmm_call == 'ab'):
            naaab += 1.0
        elif(hapmart_call == 'aa' and crlmm_call == 'bb'):
            naabb += 1.0
        
        elif(hapmart_call == 'ab' and crlmm_call == 'aa'):
            nabaa += 1.0
        elif(hapmart_call == 'ab' and crlmm_call == 'ab'):
            nabab += 1.0
        elif(hapmart_call == 'ab' and crlmm_call == 'bb'):
            nabbb += 1.0
        
        elif(hapmart_call == 'bb' and crlmm_call == 'aa'):
            nbbaa += 1.0
        elif(hapmart_call == 'bb' and crlmm_call == 'ab'):
            nbbab += 1.0
        elif(hapmart_call == 'bb' and crlmm_call == 'bb'):
            nbbbb += 1.0
hapmartfile.close()



print 'HapMap\CRLMM\tAA\tAB\tBB'
print 'AA\t\t%d\t%d\t%d' % (naaaa, naaab, naabb)
print 'AB\t\t%d\t%d\t%d' % (nabaa, nabab, nabbb)
print 'BB\t\t%d\t%d\t%d' % (nbbaa, nbbab, nbbbb)

tot1 = naaaa+naaab+naabb
tot2 = nabaa+nabab+nabbb
tot3 = nbbaa+nbbab+nbbbb
overallacc = (naaaa+nabab+nbbbb)/(tot1+tot2+tot3)
print overallacc

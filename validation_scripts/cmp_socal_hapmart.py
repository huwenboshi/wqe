#!/usr/bin/python

from optparse import OptionParser
import sys
import math
import time

# get command line
parser = OptionParser()
parser.add_option("-a", "--hapmart", dest="hapmartfile")
parser.add_option("-c", "--socal", dest="socalfile")
parser.add_option("-s", "--snps", dest="snpsfile")
parser.add_option("-m", "--map", dest="mapfile")

(options, args) = parser.parse_args()

hapmartfile_nm = options.hapmartfile
socalfile_nm = options.socalfile
snpsfile_nm = options.snpsfile
mapfile_nm = options.mapfile

# check command line
if(hapmartfile_nm == None or socalfile_nm == None or
   snpsfile_nm == None or mapfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -a to specify hapmartfile\n")
    sys.stderr.write("\tUse -c to specify socalfile\n")
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
    
    # compare with socal
    socal_indv_geno = socal_snp_indv_geno[snpid]
    for indv in socal_indv_geno:
        if(indv not in hapmart_indv_geno):
            continue
        socal_call = socal_indv_geno[indv]
        hapmart_call = hapmart_indv_geno[indv]
        
        if(hapmart_call == 'aa' and socal_call == 'aa'):
            naaaa += 1.0
        elif(hapmart_call == 'aa' and socal_call == 'ab'):
            naaab += 1.0
        elif(hapmart_call == 'aa' and socal_call == 'bb'):
            naabb += 1.0
        
        elif(hapmart_call == 'ab' and socal_call == 'aa'):
            nabaa += 1.0
        elif(hapmart_call == 'ab' and socal_call == 'ab'):
            nabab += 1.0
        elif(hapmart_call == 'ab' and socal_call == 'bb'):
            nabbb += 1.0
        
        elif(hapmart_call == 'bb' and socal_call == 'aa'):
            nbbaa += 1.0
        elif(hapmart_call == 'bb' and socal_call == 'ab'):
            nbbab += 1.0
        elif(hapmart_call == 'bb' and socal_call == 'bb'):
            nbbbb += 1.0
hapmartfile.close()



print 'HapMap\socal\tAA\tAB\tBB'
print 'AA\t\t%d\t%d\t%d' % (naaaa, naaab, naabb)
print 'AB\t\t%d\t%d\t%d' % (nabaa, nabab, nabbb)
print 'BB\t\t%d\t%d\t%d' % (nbbaa, nbbab, nbbbb)

tot1 = naaaa+naaab+naabb
tot2 = nabaa+nabab+nabbb
tot3 = nbbaa+nbbab+nbbbb
overallacc = (naaaa+nabab+nbbbb)/(tot1+tot2+tot3)
print overallacc

#!/usr/bin/python

from optparse import OptionParser
from random import shuffle
import sys
import math
import time
import numpy as np

# get command line
parser = OptionParser()
parser.add_option("-f", "--fullfile", dest="fullfile")
parser.add_option("-o", "--outfile", dest="outfile")
parser.add_option("-s", "--snps", dest="snps")
parser.add_option("-v", "--var", dest="var")
(options, args) = parser.parse_args()
fullfile_nm = options.fullfile
outfile_nm = options.outfile
snps_nm = options.snps
var = options.var


# compute mean
def get_mean(x):
    mx = [0, 0]
    for i in xrange(len(x)):
        mx[0] += x[i][0]
        mx[1] += x[i][1]
    mx[0] = mx[0]/len(x)
    mx[1] = mx[1]/len(x)
    return mx

# check command line
if(fullfile_nm == None or outfile_nm == None or
   snps_nm == None or var == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -f to specify fullfile\n")
    sys.stderr.write("\tUse -o to specify outfile\n")
    sys.stderr.write("\tUse -s to specify snps file\n")
    sys.stderr.write("\tUse -v to specify value for var\n")
    sys.exit()

var = float(var)

# load in snps
snps_set = set()
snps_file = open(snps_nm, 'r')
for line in snps_file:
    line = line.strip()
    snps_set.add(line)
snps_file.close()

# file for saving the result
outfile = open(outfile_nm,'w')
indv_list = []
fullfile = open(fullfile_nm, 'r')
flr = False
for line in fullfile:

    # get line
    line = line.strip()
    cols = line.split()
    
    # get individuals
    if(flr == False):
        flr = True
        indv_list = cols
        outfile.write(line+'\tNAA\tNAB\tNBB\n')
        continue
    
    # get snp id
    snp = cols[0]
    indv_geno = dict()

    # skip snp not selected
    if(snp not in snps_set):
        continue

    # get snp information - alleles and frequency
    sensea = cols[1][0]
    senseb = cols[1][2]
    freq = cols[2]

    # parse out training data
    paa = []
    pab = []
    pbb = []
    for i in xrange(len(indv_list)):
        info = cols[i+3].split(':')
        geno = info[1]
        sensea_int = float(info[0].split('/')[0])
        senseb_int = float(info[0].split('/')[1])
        if(geno == 'NN'):
            continue
        else:
            if(geno == sensea+sensea):
                paa.append([sensea_int, senseb_int])
            elif(geno == sensea+senseb or geno == senseb+sensea):
                pab.append([sensea_int, senseb_int])
            elif(geno == senseb+senseb):
                pbb.append([sensea_int, senseb_int])

    # obtain mean for paa, pab, and pbb
    m_aa = get_mean(paa)
    m_ab = get_mean(pab)
    m_bb = get_mean(pbb)
    
    # generate noise
    cov = [[1*var,0],[0,1*var]]
    noise_aa = np.random.multivariate_normal(m_aa,cov,1)[0]
    noise_ab = np.random.multivariate_normal(m_ab,cov,1)[0]
    noise_bb = np.random.multivariate_normal(m_bb,cov,1)[0]
    
    geno_aa = sensea+sensea
    geno_ab = sensea+senseb
    geno_bb = senseb+senseb
    outfile.write(line+'\t'+str(noise_aa[0])+'/'+str(noise_aa[1])+':'+geno_aa)
    outfile.write(line+'\t'+str(noise_ab[0])+'/'+str(noise_ab[1])+':'+geno_ab)
    outfile.write(line+'\t'+str(noise_bb[0])+'/'+str(noise_bb[1])+':'+geno_bb)
    outfile.write('\n')

# finishing up
fullfile.close()
outfile.close()

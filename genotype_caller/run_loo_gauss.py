#!/usr/bin/python

from gauss_caller import *
from cvxopt import matrix
from optparse import OptionParser
from random import shuffle
from gauss_trainer import *
import sys
import math
import time

# get command line
parser = OptionParser()
parser.add_option("-f", "--fullfile", dest="fullfile")
parser.add_option("-o", "--outfile", dest="outfile")
(options, args) = parser.parse_args()
fullfile_nm = options.fullfile
outfile_nm = options.outfile

# check command line
if(fullfile_nm == None or outfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -f to specify fullfile\n")
    sys.stderr.write("\tUse -o to specify outfile\n")
    sys.exit()

# files for saving the result
outfile = open(outfile_nm,'w')

# read in data
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
        continue
    indv_geno = dict()

    # get snp id
    snp = cols[0]

    # get snp information - alleles and frequency
    sensea = cols[1][0]
    senseb = cols[1][2]
    freq = cols[2]
    
    outline = snp+'\t'+freq+'\t'
    
    # parse out genotype information
    naa = 0
    nab = 0
    nbb = 0
    used_indv = []
    for i in xrange(len(indv_list)):
        info = cols[i+3].split(':')
        geno = info[1]
        sensea_int = info[0].split('/')[0]
        senseb_int = info[0].split('/')[1]
        if(geno == 'NN'):
            continue
        else:
            used_indv.append(indv_list[i])
            if(geno == sensea+sensea):
                naa += 1
                indv_geno[indv_list[i]] = (sensea_int,senseb_int,'aa')
            elif(geno == sensea+senseb or geno == senseb+sensea):
                nab += 1
                indv_geno[indv_list[i]] = (sensea_int,senseb_int,'ab')
            else:
                nbb += 1
                indv_geno[indv_list[i]] = (sensea_int,senseb_int,'bb')
    
    outline += str(naa)+','+str(nab)+','+str(nbb)+'\t'
    outline += ','.join(used_indv)+'\t'
    outfile.write(outline)
    
    # get training individuals and validation individuals
    for i in xrange(len(used_indv)):
    
        # select training individuals and leave-one-out validating individual
        tindv = used_indv[0:i]+used_indv[i+1:]
        vindv = used_indv[i]
        
        # train gauss
        paa = []
        pab = []
        pbb = []
        for ind in tindv:
            info = indv_geno[ind]
            genotype = info[2]
            if(genotype == 'aa'):
                paa.append([float(info[0]), float(info[1])])
            elif(genotype == 'ab'):
                pab.append([float(info[0]), float(info[1])])
            elif(genotype == 'bb'):
                pbb.append([float(info[0]), float(info[1])])
        
        trainer = gauss_trainer(paa, pab, pbb)
        
        # time execution in ms
        t1 = time.time()
        trainer.train()
        t2 = time.time()
        dt = (t2-t1)*1000.0
        
        # get truth
        info = indv_geno[vindv]
        truth = info[2]
        
        # get the ellipsoids - skip the ellipsoid if any cluster can't be
        # estimated
        ellipsoids = trainer.get_gauss_params()
        e_aa = ellipsoids['aa']
        e_ab = ellipsoids['ab']
        e_bb = ellipsoids['bb']
        
        # run the caller
        c_aa = None
        E_aa = None
        c_ab = None
        E_ab = None
        c_bb = None
        E_bb = None
        if(e_aa != None):
            c_aa = e_aa['m']
            E_aa = e_aa['cov']
        if(e_ab != None):
            c_ab = e_ab['m']
            E_ab = e_ab['cov']
        if(e_bb != None):
            c_bb = e_bb['m']
            E_bb = e_bb['cov']
        sc = gauss_caller(c_aa,E_aa,c_ab,E_ab,c_bb,E_bb)
        
        # do calling
        x = matrix([float(info[0]),float(info[1])],(2,1))
        result = sc.mindist(x)
        call = result[0]
        score = result[1]
        
        # write out result
        outfile.write(truth+'/'+call+','+str(score)+','+str(dt))
        if(i != len(used_indv)-1):
            outfile.write('\t')
    outfile.write('\n')
        
fullfile.close()
outfile.close()

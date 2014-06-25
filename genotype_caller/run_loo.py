#!/usr/bin/python

from socal_caller import *
from cvxopt import matrix
from optparse import OptionParser
from random import shuffle
from socal_trainer import *
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
                indv_geno[indv_list[i]] = (sensea_int,senseb_int,'aa')
            elif(geno == sensea+senseb):
                indv_geno[indv_list[i]] = (sensea_int,senseb_int,'ab')
            else:
                indv_geno[indv_list[i]] = (sensea_int,senseb_int,'bb')
    
    outline += ','.join(used_indv)+'\t'
    outfile.write(outline)
    
    # get training individuals and validation individuals
    for i in xrange(len(used_indv)):
    
        # select training individuals and leave-one-out validating individual
        tindv = used_indv[0:i]+used_indv[i+1:]
        vindv = used_indv[i]
        
        # train socal
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
        c1 = 1
        c2 = 10
        c3 = 100
        
        trainer = socal_trainer(snp, paa, pab, pbb, c1, c2, c3)
        
        # time execution in ms
        t1 = time.time()
        trainer.train()
        trainer.rescue()
        t2 = time.time()
        dt = (t2-t1)*1000.0
        
        # get the ellipsoids - skip the ellipsoid if any cluster can't be
        # estimated
        ellipsoids = trainer.get_ellipsoids()
        e_aa = ellipsoids['aa']
        e_ab = ellipsoids['ab']
        e_bb = ellipsoids['bb']
        if(e_aa == None or e_ab == None or e_bb == None):
            continue
        
        # run the caller
        c_aa = e_aa['c']
        E_aa = e_aa['E']
        c_ab = e_ab['c']
        E_ab = e_ab['E']
        c_bb = e_bb['c']
        E_bb = e_bb['E']
        sc = socal_caller(c_aa,E_aa,c_ab,E_ab,c_bb,E_ab,30)
        
        # do validation
        info = indv_geno[vindv]
        truth = info[2]
        x = matrix([float(info[0]),float(info[1])],(2,1))
        result = sc.mindist(x)
        
        call = result[0]
        score = result[1]
        
        # write out result
        outfile.write(truth+'/'+call+','+str(score)+','+str(dt))
        if(i != len(indv_list)-1):
            outfile.write('\t')
        else:
            outfile.write('\n')
        
fullfile.close()
outfile.close()
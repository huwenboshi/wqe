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
parser.add_option("-a", "--aval", dest="aval_str")
parser.add_option("-b", "--bval", dest="bval_str")
parser.add_option("-c", "--cval", dest="cval_str")
parser.add_option("-d", "--dval", dest="dval_str")
parser.add_option("-e", "--eval", dest="eval_str")
(options, args) = parser.parse_args()
fullfile_nm = options.fullfile
outfile_nm = options.outfile
aval = options.aval_str
bval = options.bval_str
cval = options.cval_str
dval = options.dval_str
evalu = options.eval_str

# check command line
if(fullfile_nm == None or outfile_nm == None or
   aval == None or bval == None or cval == None or
   dval == None or evalu == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -f to specify fullfile\n")
    sys.stderr.write("\tUse -o to specify outfile\n")
    sys.stderr.write("\tUse -a to specify aval\n")
    sys.stderr.write("\tUse -b to specify bval\n")
    sys.stderr.write("\tUse -c to specify cval\n")
    sys.stderr.write("\tUse -d to specify dval\n")
    sys.stderr.write("\tUse -e to specify eval\n")
    sys.exit()

# files for saving the result
outfile = open(outfile_nm,'w')

# parameters
c1 = float(aval)
c2 = float(bval)
c3 = float(cval)
c4 = float(dval)
c5 = float(evalu)

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
        
        trainer = socal_trainer(snp, paa, pab, pbb, c1, c2, c3)
        
        # time execution in ms
        t1 = time.time()
        trainer.train()
        trainer.rescue(c5)
        t2 = time.time()
        dt = (t2-t1)*1000.0
        
        # get truth
        info = indv_geno[vindv]
        truth = info[2]
        
        # get the ellipsoids - skip the ellipsoid if any cluster can't be
        # estimated
        ellipsoids = trainer.get_ellipsoids()
        e_aa = ellipsoids['aa']
        e_ab = ellipsoids['ab']
        e_bb = ellipsoids['bb']
        if(e_aa == None or e_ab == None or e_bb == None):
            outfile.write(truth+'/NN')
            if(i != len(used_indv)-1):
                outfile.write('\t')
            continue
        
        # run the caller
        c_aa = e_aa['c']
        E_aa = e_aa['E']
        c_ab = e_ab['c']
        E_ab = e_ab['E']
        c_bb = e_bb['c']
        E_bb = e_bb['E']
        sc = socal_caller(c_aa,E_aa,c_ab,E_ab,c_bb,E_ab,c4)
        
        # do validation
        x = matrix([float(info[0]),float(info[1])],(2,1))
        result = sc.mindist(x)
        
        if(result == None):
            outfile.write(truth+'/NN')
            if(i != len(used_indv)-1):
                outfile.write('\t')
            continue
        
        call = result[0]
        score = result[1]
        
        # write out result
        outfile.write(truth+'/'+call+','+str(score)+','+str(dt))
        if(i != len(used_indv)-1):
            outfile.write('\t')
    outfile.write('\n')
        
fullfile.close()
outfile.close()

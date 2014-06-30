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
outfile_call = open(outfile_nm+'_call.txt','w')
outfile_conf = open(outfile_nm+'_conf.txt','w')

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
        outfile_call.write('\t'.join(indv_list)+'\n')
        outfile_conf.write('\t'.join(indv_list)+'\n')
        continue

    # get snp id
    snp = cols[0]
    
    # get snp alleles
    sensea = cols[1][0]
    senseb = cols[1][2]
    
    # write out snp ids
    outfile_call.write(snp+'\t')
    outfile_conf.write(snp+'\t')

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
            else:
                pbb.append([sensea_int, senseb_int])
    
    # train caller
    trainer = socal_trainer(snp, paa, pab, pbb, c1, c2, c3)
    trainer.train()
    trainer.rescue(c5)
    
    # get the ellipsoids - skip the ellipsoid if any cluster can't be
    # estimated
    ellipsoids = trainer.get_ellipsoids()
    e_aa = ellipsoids['aa']
    e_ab = ellipsoids['ab']
    e_bb = ellipsoids['bb']
    
    # create the caller
    c_aa = None
    E_aa = None
    c_ab = None
    E_ab = None
    c_bb = None
    E_bb = None
    if(e_aa != None):
        c_aa = e_aa['c']
        E_aa = e_aa['E']
    if(e_ab != None):
        c_ab = e_ab['c']
        E_ab = e_ab['E']
    if(e_bb != None):
        c_bb = e_bb['c']
        E_bb = e_bb['E']
    sc = socal_caller(c_aa,E_aa,c_ab,E_ab,c_bb,E_bb,c4,e_aa,e_ab,e_bb)
    
    # run the caller
    for i in xrange(len(indv_list)):
        info = cols[i+3].split(':')
        geno = info[1]
        sensea_int = float(info[0].split('/')[0])
        senseb_int = float(info[0].split('/')[1])
        
        # do calling
        x = matrix([sensea_int, senseb_int],(2,1))
        result = sc.mindist(x)
        call = result[0]
        score = result[1]
        
        # write out to file
        outfile_call.write(call+'\t')
        outfile_conf.write(str(score)+'\t')
    
    outfile_call.write('\n')
    outfile_conf.write('\n')
        
fullfile.close()
outfile_call.close()
outfile_conf.close()

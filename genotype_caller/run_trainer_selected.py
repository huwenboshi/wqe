#!/usr/bin/python

from optparse import OptionParser
from random import shuffle
from socal_trainer import *
import sys
import math
import time

# get command line
parser = OptionParser()
parser.add_option("-f", "--fullfile", dest="fullfile")
parser.add_option("-t", "--trainpct", dest="trainpct")
parser.add_option("-s", "--snpfile", dest="snpfile")

(options, args) = parser.parse_args()
fullfile_nm = options.fullfile
trainpct_str = options.trainpct
snpfile_nm = options.snpfile

# check command line
if(fullfile_nm == None or trainpct_str == None or snpfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -f to specify fullfile\n")
    sys.stderr.write("\tUse -t to specify trainpct\n")
    sys.stderr.write("\tUse -s to specify snpfile\n")
    sys.exit()

# files for saving the result
tvinf_file_nm = 'trainpct_'+trainpct_str+'_tvinfo.txt'
tvinf_file = open(tvinf_file_nm, 'w')
ellipsoid_file_nm = 'trainpct_'+trainpct_str+'_ellipsoids.txt'
ellipsoid_file = open(ellipsoid_file_nm,'w')

# read in snp set
snpfile = open(snpfile_nm, 'r')
snp_set = set()
for line in snpfile:
    line = line.strip()
    snp_set.add(line)
snpfile.close()

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
    if(snp not in snp_set):
        continue

    # get snp information - alleles and frequency
    sensea = cols[1][0]
    senseb = cols[1][2]
    freq = cols[2]
    
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
            elif(geno == sensea+senseb or geno == senseb+sensea):
                indv_geno[indv_list[i]] = (sensea_int,senseb_int,'ab')
            else:
                indv_geno[indv_list[i]] = (sensea_int,senseb_int,'bb')
    
    # get training individuals and validation individuals
    tf = float(trainpct_str)/100
    tn = int(math.floor(tf*len(used_indv)))
    vn = len(used_indv)-tn
    shuffle(used_indv)
    tindv = used_indv[0:tn]
    vindv = used_indv[tn:len(used_indv)]
    
    # write to tvinf_file
    tvinf_line = snp+'\t'+','.join(tindv)+'\t'+','.join(vindv)+'\n'
    tvinf_file.write(tvinf_line)
    
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
    c2 = 10000
    c3 = 100
    trainer = socal_trainer(snp, paa, pab, pbb, c1, c2, c3)
    
    # time execution in ms
    t1 = time.time()
    trainer.train()
    trainer.rescue(1.0)
    t2 = time.time()
    dt = (t2-t1)*1000.0
    
    # get the ellipsoids
    ellipsoids = trainer.get_ellipsoids()
    
    # write to ellipsoid file
    ellipsoid_line = snp+'\t'+str(freq)+'\t'+str(dt)+'\t'
    e_aa = ellipsoids['aa']
    if(e_aa != None):
        c = e_aa['c']
        ellipsoid_line += str(c[0])+','+str(c[1])+','
        E = e_aa['E']
        ellipsoid_line += str(E[0,0])+','+str(E[0,1])+','+str(E[1,0])+','
        ellipsoid_line += str(E[1,1])+','
        rho = e_aa['rho']
        ellipsoid_line += str(rho)+'\t'
    else:
        ellipsoid_line += ','.join(['-1.0']*6)+'\t'
        
    e_ab = ellipsoids['ab']
    if(e_ab != None):
        c = e_ab['c']
        ellipsoid_line += str(c[0])+','+str(c[1])+','
        E = e_ab['E']
        ellipsoid_line += str(E[0,0])+','+str(E[0,1])+','+str(E[1,0])+','
        ellipsoid_line += str(E[1,1])+','
        rho = e_ab['rho']
        ellipsoid_line += str(rho)+'\t'
    else:
        ellipsoid_line += ','.join(['-1.0']*6)+'\t'
        
    e_bb = ellipsoids['bb']
    if(e_bb != None):
        c = e_bb['c']
        ellipsoid_line += str(c[0])+','+str(c[1])+','
        E = e_bb['E']
        ellipsoid_line += str(E[0,0])+','+str(E[0,1])+','+str(E[1,0])+','
        ellipsoid_line += str(E[1,1])+','
        rho = e_bb['rho']
        ellipsoid_line += str(rho)
    else:
        ellipsoid_line += ','.join(['-1.0']*6)
    
    # write result to file
    ellipsoid_line += '\n'
    ellipsoid_file.write(ellipsoid_line)

fullfile.close()
tvinf_file.close()
ellipsoid_file.close()

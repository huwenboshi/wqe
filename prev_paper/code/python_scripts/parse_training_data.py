#!/usr/bin/python

import sys
import math
from optparse import OptionParser
from random import shuffle

parser = OptionParser()
parser.add_option("-f", "--fullfile", dest="fullfile")
parser.add_option("-t", "--trainpct", dest="trainpct")
parser.add_option("-v", "--validatepct", dest="validatepct")

(options, args) = parser.parse_args()

fullfile_nm = options.fullfile
trainpct_str = options.trainpct
validatepct_str = options.validatepct

if(fullfile_nm == None or trainpct_str == None or validatepct_str == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -f to specify fullfile\n")
    sys.stderr.write("\tUse -t to specify trainpct\n")
    sys.stderr.write("\tUse -v to specify validatepct\n")
    sys.exit()

maxsnp = 5000
nsnp = 0

indv_list = []
fullfile = open(fullfile_nm, 'r')
flr = False
for line in fullfile:
    line = line.strip()
    cols = line.split()
    if(flr == False):
        flr = True
        indv_list = cols
        continue
    indv_geno = dict()
    snp = cols[0]
    
    nsnp += 1
    if(nsnp > maxsnp):
        break

    sensea = cols[1][0]
    senseb = cols[1][2]
    freq = cols[2]
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
                indv_geno[indv_list[i]] = (sensea_int,senseb_int,1)
            elif(geno == sensea+senseb):
                indv_geno[indv_list[i]] = (sensea_int,senseb_int,2)
            else:
                indv_geno[indv_list[i]] = (sensea_int,senseb_int,3)
    tf = float(trainpct_str)/100
    vf = float(validatepct_str)/100
    tn = int(math.floor(tf*len(used_indv)))
    vn = len(used_indv)-tn
    shuffle(used_indv)
    tindv = used_indv[0:tn]
    vindv = used_indv[tn:len(used_indv)]
    tfnm = snp+'_train.txt'
    tfnm_file = open(tfnm,'w')
    for ind in tindv:
        info = indv_geno[ind]
        tfnm_file.write(info[0]+','+info[1]+','+str(info[2])+'\n')
    tfnm_file.close()

    vfnm = snp+'_validate.txt'
    vfnm_file = open(vfnm,'w')
    for ind in vindv:
        info = indv_geno[ind]
        vfnm_file.write(info[0]+','+info[1]+','+str(info[2])+'\n')
    vfnm_file.close()
fullfile.close()


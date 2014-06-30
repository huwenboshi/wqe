#!/usr/bin/python

from optparse import OptionParser
import sys

# get command line
parser = OptionParser()
parser.add_option("-f", "--fullfile", dest="fullfile")
parser.add_option("-t", "--threshold", dest="threshold")
(options, args) = parser.parse_args()
fullfile_nm = options.fullfile
threshold_str = options.threshold

# default threshold value
if(threshold_str == None):
    threshold_str = '20'

# check command line
if(fullfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -f to specify fullfile\n")
    sys.stderr.write("\tUse -t to specify threshold\n")
    sys.exit()

threshold = int(threshold_str)

# read in data
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
    
    naa = 0
    nab = 0
    nbb = 0
    
    # parse out genotype information
    for i in xrange(len(indv_list)):
        info = cols[i+3].split(':')
        geno = info[1]
        sensea_int = info[0].split('/')[0]
        senseb_int = info[0].split('/')[1]
        if(geno == 'NN'):
            continue
        else:
            if(geno == sensea+sensea):
                naa += 1
            elif(geno == sensea+senseb or geno == senseb+sensea):
                nab += 1
            else:
                nbb += 1
    
    if(naa >= threshold and nab >=  threshold and nbb >= threshold):
        print snp

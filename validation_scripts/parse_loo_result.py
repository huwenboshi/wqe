#!/usr/bin/python

from optparse import OptionParser
import sys
import math
import time

# get command line
parser = OptionParser()
parser.add_option("-l", "--loofile", dest="loofile")
parser.add_option("-t", "--threshold", dest="threshold")
parser.add_option("-o", "--outfile", dest="outfile")
(options, args) = parser.parse_args()
loofile_nm = options.loofile
outfile_nm = options.outfile
threshold_str = options.threshold

# set default value for confidence score threshold
if(threshold_str == None):
    threshold_str = "0.0"

# check command line
if(loofile_nm == None or outfile_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -l to specify loofile\n")
    sys.stderr.write("\tUse -o to specify outfile\n")
    sys.stderr.write("\tUse -t to specify score threshold\n")
    sys.exit()

# parse threshold
threshold = float(threshold_str)

# result
naaaa = 0.0
naaab = 0.0
naabb = 0.0

nabaa = 0.0
nabab = 0.0
nabbb = 0.0

nbbaa = 0.0
nbbab = 0.0
nbbbb = 0.0

nnc = 0.0

ntot = 0.0

loofile = open(loofile_nm, 'r')
for line in loofile:

    # get snp information
    line = line.strip()
    cols = line.split('\t')
    snpid= cols[0]
    freq = float(cols[1])
    
    # skip monomorphic snps
    #if(freq >= 0.99 or freq <= 0.01):
    #    continue

    # get data counts    
    cnts = cols[2].split(',')
    
    # count the number of missing clusters
    nmissing = 0
    for i in xrange(len(cnts)):
        if(int(cnts[i]) < 5):
            nmissing += 1
    
    # if missing 2 or more clusters, skip
    if(nmissing >= 2):
        continue
    
    # parse result
    for i in xrange(4,len(cols)):
    
        # count total call
        ntot += 1.0
    
        # skip no call
        if(cols[i] == 'NN/NN'):
            nnc += 1.0
            continue
    
        # parse result with call
        results = cols[i].split(',')
        tp = results[0].split('/')
        truth = tp[0]
        pred = tp[1]
        score = float(results[1])
        if(score >= threshold):
            if(truth == 'aa' and pred == 'aa'):
                naaaa += 1.0
            elif(truth == 'aa' and pred == 'ab'):
                naaab += 1.0
            elif(truth == 'aa' and pred == 'bb'):
                naabb += 1.0
            elif(truth == 'ab' and pred == 'aa'):
                nabaa += 1.0
            elif(truth == 'ab' and pred == 'ab'):
                nabab += 1.0
            elif(truth == 'ab' and pred == 'bb'):
                nabbb += 1.0
            elif(truth == 'bb' and pred == 'aa'):
                nbbaa += 1.0
            elif(truth == 'bb' and pred == 'ab'):
                nbbab += 1.0
            elif(truth == 'bb' and pred == 'bb'):
                nbbbb += 1.0
            else:
                nnc += 1.0
loofile.close()

print '%f\t%f\t%f' % (naaaa, naaab, naabb)
print '%f\t%f\t%f' % (nabaa, nabab, nabbb)
print '%f\t%f\t%f' % (nbbaa, nbbab, nbbbb)

# compute overall accuracy
tot1 = naaaa+naaab+naabb
tot2 = nabaa+nabab+nabbb
tot3 = nbbaa+nbbab+nbbbb
call_rate = (tot1+tot2+tot3)/(ntot)
overallacc = (naaaa+nabab+nbbbb)/(tot1+tot2+tot3)

print 'call rate: %f' % call_rate
print 'overall accuracy: %f' % overallacc

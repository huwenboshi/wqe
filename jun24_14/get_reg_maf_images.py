#!/usr/bin/python

import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils import *

# load sense a data
sense_a_data = load_intensity_file('/u/home/s/shihuwen/project/wqe/affy100k_intensity/affy100k_hind_sense_a_intensity.txt')
sense_a_int = sense_a_data[0]
sense_a_snps = sense_a_data[1]
sense_a_inds = set(sense_a_data[2])

# load sense b data
sense_b_data = load_intensity_file('/u/home/s/shihuwen/project/wqe/affy100k_intensity/affy100k_hind_sense_b_intensity.txt')
sense_b_int = sense_b_data[0]
sense_b_snps = sense_b_data[1]
sense_b_inds = set(sense_b_data[2])

# get snps in common
in_common_snps = sense_a_snps.intersection(sense_b_snps)
in_common_inds = sense_a_inds.intersection(sense_b_inds)

# load low maf snps
low_maf_snps = set()
f = open('reg_maf_snps.txt', 'r')
for line in f:
    line = line.strip()
    low_maf_snps.add(line)
f.close()

# generate plots
count = 0
for snp in in_common_snps:
    if(snp not in low_maf_snps):
        continue
    f = open(snp+'int.txt', 'w')
    if(count > 100):
        break
    points_sense_a = []
    points_sense_b = []
    for ind in in_common_inds:
        points_sense_a.append(sense_a_int[snp][ind])
        points_sense_b.append(sense_b_int[snp][ind])
        f.write(str(sense_a_int[snp][ind])+', '+str(sense_b_int[snp][ind])+'\n')
    f.close()
    plt.plot(points_sense_a, points_sense_b, 'r.')
    plt.xlabel('Allele A Intensity')
    plt.ylabel('Allele B Intensity')
    plt.savefig(snp+'_HIND.png')
    count += 1
    plt.clf()


from maxsep_caller import *
from comb_caller import *

# load training data
train_data_file = open('../test_data/SNP_A-1643086_train.txt', 'r')
pa = []
pb = []
for line in train_data_file:
    line = line.strip()
    cols = line.split(',')
    gentype = cols[2]
    if(gentype == '3'):
        pa.append([float(cols[0]), float(cols[1])])
    else:
        pb.append([float(cols[0]), float(cols[1])])

c1 = 1
c2 = 10
c3 = 100
a = comb_caller('SNP_A-1643086', pa, pb, c1, c2, c3)
a.find_ellipsoid()

from maxsep_caller import *

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

a = maxsep_caller('SNP_A-1643086', pa, pb)
a.find_ellipsoid()

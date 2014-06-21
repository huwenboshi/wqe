from maxsep import *
from robsep import *

# load training data
train_data_file = open('../test_data/SNP_A-1643086_train.txt', 'r')
pa = []
pb = []
for line in train_data_file:
    line = line.strip()
    cols = line.split(',')
    gentype = cols[2]
    if(gentype == '1'):
        pa.append([float(cols[0]), float(cols[1])])
    else:
        pb.append([float(cols[0]), float(cols[1])])

c1 = 1
c2 = 10
c3 = 100
a = robsep(pa, pb, c1, c2, c3)
b = maxsep(pa, pb)
(c1, E1, rho1) = a.find_ellipsoid()
(c2, E2, rho2) = b.find_ellipsoid()


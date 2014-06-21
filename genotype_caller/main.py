from maxsep import *
from robsep import *
from socal_trainer import *

# load training data
train_data_file = open('../test_data/SNP_A-1643086_train.txt', 'r')
paa = []
pab = []
pbb = []
for line in train_data_file:
    line = line.strip()
    cols = line.split(',')
    genotype = cols[2]
    if(genotype == '1'):
        paa.append([float(cols[0]), float(cols[1])])
    elif(genotype == '2'):
        pab.append([float(cols[0]), float(cols[1])])
    elif(genotype == '3'):
        pbb.append([float(cols[0]), float(cols[1])])

c1 = 1
c2 = 10
c3 = 100
st = socal_trainer('SNP_A-1643086', paa, pab, pbb, c1, c2, c3)
st.train()


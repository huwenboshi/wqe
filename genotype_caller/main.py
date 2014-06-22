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
    if(genotype == '2'):
        paa.append([float(cols[0]), float(cols[1])])
    elif(genotype == '1'):
        pab.append([float(cols[0]), float(cols[1])])
    elif(genotype == '3'):
        pbb.append([float(cols[0]), float(cols[1])])

c1 = 1
c2 = 10
c3 = 100
trainer = socal_trainer('SNP_A-1643086', paa, pab, pbb, c1, c2, c3)
trainer.train()
trainer.rescue()
ellipsoids = trainer.get_ellipsoids()
e_aa = ellipsoids['aa']
print 'aa'
print e_aa['c']
print e_aa['E']
print
print 'ab'
e_ab = ellipsoids['ab']
print e_ab['c']
print e_ab['E']
print
print 'bb'
e_bb = ellipsoids['bb']
print e_bb['c']
print e_bb['E']

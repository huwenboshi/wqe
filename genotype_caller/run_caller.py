from socal_caller import *
from cvxopt import matrix

c_aa = matrix([0,0],(2,1))
E_aa = matrix([1,0,0,1],(2,2))

c_ab = matrix([1,1],(2,1))
E_ab = matrix([1,0,0,1],(2,2))

c_bb = matrix([2,2],(2,1))
E_bb = matrix([1,0,0,1],(2,2))

sc = socal_caller('test', c_aa,E_aa,c_ab,E_ab,c_bb,E_ab,32)
xs = [matrix([0,0],(2,1)),matrix([1,1],(2,1)),matrix([2,2],(2,1))]

for x in xs:
    print sc.mindist(x)

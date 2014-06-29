from cvxopt import matrix
import math
import numpy as np

def dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))

def length(v):
    return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
    return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))
  
def rot_mat(ang):
    m = matrix(np.matrix([[math.cos(ang), -math.sin(ang)],
                          [math.sin(ang),  math.cos(ang)]]))
    return m

def get_unit_vec(vec):
    return matrix(vec/math.sqrt(np.dot(vec,vec)))
    
def mean_ps(ps):
    nrow = ps.size[0]
    ncol = ps.size[1]

    means = [0.0]*nrow    
    for i in xrange(0, ncol):
        for j in xrange(0, nrow):
            means[j] += ps[j,i]/float(ncol)
    
    return matrix(means, (1,nrow))

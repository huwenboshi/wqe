from cvxopt import matrix, spmatrix, solvers
from cvxopt.lapack import gesv, getrs
from numpy import array
import numpy
import math
import time

# quiet cvxopt
solvers.options['show_progress'] = False

# ellipsoidal separation using maxsep
class maxsep:
    
    # default constructor
    def __init__(self):
        return
    
    # setter for parameters
    def set_param(self, pa, pb):
        self.pa = matrix(pa)
        self.pb = matrix(pb)
    
    # initialize the maxsep
    # pa - na*dim matrix containing points to be included in the ellipsoid
    # pb - nb*dim matrix containing points to be excluded in the ellipsoid
    def __init__(self, pa, pb):
        self.set_param(pa, pb)
    
    # transform into homogeneous coordinate
    # add a row of 1 vector to p
    def homogenize(self, p):
        nrow = p.size[0]
        ncol = p.size[1]
        nrow = nrow + 1
        hp = matrix([1.0]*(nrow*ncol), (nrow, ncol))
        hp[1:,0:] = p
        return hp
    
    # obtain ellipsoid using cvxopt
    def find_ellipsoid(self):
        
        # homogenize coordinates
        pah = self.homogenize(self.pa)
        pbh = self.homogenize(self.pb)
        dim = pah.size[0]
        num_pah = pah.size[1]
        num_pbh = pbh.size[1]
        
        # get the c vector
        c = matrix([-1.0]+[0.0]*(dim*dim), (1+dim*dim,1))
        
        # get Gl and hl
        # separation constraint
        Gl_t = []
        for i in xrange(num_pah):
            row = [0.0]
            for j in xrange(dim):
                for k in xrange(dim):
                    row.append(pah[j,i]*pah[k,i])
            Gl_t.append(row)
        for i in xrange(num_pbh):
            row = [1.0]
            for j in xrange(dim):
                for k in xrange(dim):
                    row.append(-1.0*pbh[j,i]*pbh[k,i])
            Gl_t.append(row)
        Gl = matrix(Gl_t).trans()
        hl = matrix([1.0]*num_pah+[0.0]*num_pbh,(num_pah+num_pbh,1))
        
        # get Gs and hs
        # positive semidefinite constraint
        Gs = []
        Gs.append([0.0]*(dim*dim))
        for i in xrange(dim*dim):
            v = [0.0]*(dim*dim)
            rpos = int(math.floor(float(i)/float(dim)))
            cpos = i % dim
            if(rpos == cpos):
                v[i] = -1.0
            else:
                v[i] = -0.5
                v[cpos*dim+rpos] = -0.5
            Gs.append(v)
        Gs = [matrix(Gs)]
        hs = [matrix([0.0]*(dim*dim),(dim,dim))]
        
        # get A and b
        # symmetry constraint
        A_t = []
        for i in xrange(dim):
            for j in xrange(i, dim):
                if(i != j):
                    v = [0.0]*(1+dim*dim)
                    v[1+i*dim+j] = 1.0
                    v[1+j*dim+i] = -1.0
                    A_t.append(v)
        A = matrix(A_t).trans()
        b = matrix([0.0]*A.size[0],(A.size[0],1))
        
        # solve it
        passed = False
        ntime = 1000
        while(passed == False and ntime > 0):
            try:
                sol = solvers.sdp(c, Gl, hl, Gs, hs, A, b)
                passed = True
            except ZeroDivisionError:
                time.sleep(0.001)
                ntime = ntime-1
        if(passed == False):
            return None

        # parse out solution
        x = sol['x']
        k = x[0]
        E_hat = matrix(x[1:], (dim,dim))
        F = E_hat[1:,1:]
        v = E_hat[1:,0]
        s = E_hat[0,0]
        ipiv = matrix(0, (dim-1,1))
        gesv(-F, v, ipiv)
        c = v
        btm = 1-(s-c.trans()*F*c)
        for i in xrange(F.size[0]):
            for j in xrange(F.size[1]):
                F[i,j] = F[i,j]/btm
        E = F
        rho = k
        
        # function return
        return (c, E, rho)

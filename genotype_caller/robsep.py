from cvxopt import matrix, spmatrix, solvers
from cvxopt.lapack import gesv, getrs
from numpy import array
import numpy
import math
import time

# quiet cvxopt
solvers.options['show_progress'] = False

# ellipsoidal separation using robsep
class robsep:
    
    # setter for parameters
    def set_param(self, c1, c2, c3):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
    
    # setter for data
    def set_data(self, pa, pb):
        self.pa = matrix(pa)
        self.pb = matrix(pb)
    
    # initialize the robsep
    # pa - na*dim matrix containing points to be included in the ellipsoid
    # pb - nb*dim matrix containing points to be excluded in the ellipsoid
    def __init__(self, pa=None, pb=None, c1=None, c2=None, c3=None):
        if(pa != None and pb != None):
            self.set_data(pa, pb)
        if(c1 != None and c2 != None and c3 != None):
            self.set_param( c1, c2, c3)
    
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
    
        # return None if not enough data is available
        if(self.pa.size[1] < 3 or self.pb.size[1] < 3):
            return None
        
        # homogenize coordinates
        pah = self.homogenize(self.pa)
        pbh = self.homogenize(self.pb)
        dim = pah.size[0]
        num_pah = pah.size[1]
        num_pbh = pbh.size[1]
        
        # get the c vector
        num_vars = 1+(dim-1)*(dim-1)+2*num_pah+dim*dim
        c = matrix([0.0]*num_vars, (num_vars,1))
        c[0,0] = -self.c1
        
        for i in xrange(dim-1):
            for j in xrange(dim-1):
                if(i == j):
                    c[1+i*(dim-1)+j,0] = self.c2
        for i in xrange(num_pah):
            c[1+(dim-1)*(dim-1)+i,0] = self.c3
        for i in xrange(num_pah):
            c[1+(dim-1)*(dim-1)+num_pah+i,0] = 0.0
        for i in xrange(dim*dim):
            c[1+(dim-1)*(dim-1)+num_pah+num_pah+i,0] = 0.0

        # get Gl and hl
        # separation constraint
        Gl_t = []
        for i in xrange(num_pah):
            row = [0.0]*(1+(dim-1)*(dim-1)+num_pah)+[0.0]*num_pah
            row[(1+(dim-1)*(dim-1)+num_pah)+i] = -1.0
            for j in xrange(dim):
                for k in xrange(dim):
                    row.append(pah[j,i]*pah[k,i])
            Gl_t.append(row)
        for i in xrange(num_pbh):
            row = [1.0]+[0.0]*((dim-1)*(dim-1)+2*num_pah)
            for j in xrange(dim):
                for k in xrange(dim):
                    row.append(-1.0*pbh[j,i]*pbh[k,i])
            Gl_t.append(row)
        # l1 norm constraint
        for i in xrange(num_pah):
            row = [0.0]*num_vars
            row[1+(dim-1)*(dim-1)+i] = -1.0
            row[1+(dim-1)*(dim-1)+num_pah+i] = -1.0
            Gl_t.append(row)
        for i in xrange(num_pah):
            row = [0.0]*num_vars
            row[1+(dim-1)*(dim-1)+i] = -1.0
            row[1+(dim-1)*(dim-1)+num_pah+i] = 1.0
            Gl_t.append(row)
        # construct Gl and hl
        Gl = matrix(Gl_t).trans()
        col = [0.0]*(num_pah+num_pbh)+[-1.0]*num_pah+[1.0]*num_pah
        hl = matrix(col,(3*num_pah+num_pbh,1))
        
        # get Gs and hs
        # positive semidefinite constraint
        # E must be positive semidefinite
        Gs = []
        for i in xrange(1+(dim-1)*(dim-1)+2*num_pah):
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
        
        # block matrix must be positive semidefinite
        Gs2 = []
        Gs2.append([0.0]*(((dim-1)*2)*((dim-1)*2)))
        for i in xrange((dim-1)*(dim-1)):
            v = [0.0]*(((dim-1)*2)*((dim-1)*2))
            rpos = int(math.floor(float(i)/float(dim-1)))
            cpos = i % (dim-1)
            if(rpos == cpos):
                v[(rpos+dim-1)*(dim-1)*2+(dim-1)+cpos] = -1.0
            else:
                v[(rpos+dim-1)*(dim-1)*2+(dim-1)+cpos] = -0.5
                v[(cpos+dim-1)*(dim-1)*2+(dim-1)+rpos] = -0.5
            Gs2.append(v)
            
        for i in xrange(2*num_pah):
            Gs2.append([0.0]*(((dim-1)*2)*((dim-1)*2)))
        for i in xrange(dim*dim):
            v = [0.0]*(((dim-1)*2)*((dim-1)*2))
            rpos = int(math.floor(float(i)/float(dim)))
            cpos = i % dim
            if(rpos == 0 or cpos == 0):
                Gs2.append(v)
            else:
                rpos = rpos-1
                cpos = cpos-1
                if(rpos == cpos):
                    v[rpos*(dim-1)*2+cpos] = -1.0
                else:
                    v[rpos*(dim-1)*2+cpos] = -0.5
                    v[cpos*(dim-1)*2+rpos] = -0.5
                Gs2.append(v)
            
        Gs.append(matrix(Gs2))
        zero_block = matrix([0.0]*((dim-1)*(dim-1)),((dim-1), (dim-1)))
        eye_block = spmatrix(1.0, range(dim-1), range(dim-1))
        hs2 = matrix([[zero_block, eye_block], [eye_block, zero_block]])
        hs.append(hs2)
        
        # get A and b
        # symmetry constraint
        A_t = []
        for i in xrange(dim):
            for j in xrange(i, dim):
                if(i != j):
                    v = [0.0]*(num_vars)
                    v[1+(dim-1)*(dim-1)+2*num_pah+i*dim+j] = 1.0
                    v[1+(dim-1)*(dim-1)+2*num_pah+j*dim+i] = -1.0
                    A_t.append(v)
        for i in xrange(dim-1):
            for j in xrange(i, dim-1):
                if(i != j):
                    v = [0.0]*(num_vars)
                    v[1+i*(dim-1)+j] = 1.0
                    v[1+j*(dim-1)+i] = -1.0
                    A_t.append(v)
        A = matrix(A_t).trans()
        b = matrix([0.0]*A.size[0],(A.size[0],1))
        
        # solve it
        passed = False
        ntime = 5
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
        E_hat = matrix(x[1+(dim-1)*(dim-1)+2*num_pah:], (dim,dim))
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
        return {'c':c, 'E':E, 'rho':rho}

from cvxopt import matrix, solvers
solvers.options['show_progress'] = False

import math

# genotype calling using maxsep
class maxsep_caller:
    
    # initialize the maxsep_caller
    # snpid - the id of the snp
    # pa - na*dim matrix containing points to be included in the ellipsoid
    # pb - nb*dim matrix containing points to be excluded in the ellipsoid
    def __init__(self, snpid, pa, pb):
        self.snpid = snpid
        self.pa = matrix(pa)
        self.pb = matrix(pb)
    
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
        sol = solvers.sdp(c, Gl, hl, Gs, hs, A, b)
        print(sol['x'])

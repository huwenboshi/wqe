from cvxopt import matrix, spmatrix, solvers
from cvxopt.lapack import gesv, getrs
import numpy as np
import time

# trainer for socal using ellipsoidal separation
class gauss_trainer:
    
    # initialize the genotype_trainer, using robsep
    def __init__(self, paa, pab, pbb):
        self.paa = paa
        self.pab = pab
        self.pbb = pbb
    
    # train the socal genotype caller - find ellipsoidal separator
    def train(self):
        m_aa = np.mean(self.paa, axis=0)
        cov_aa = np.cov(np.array(self.paa).T)
        m_aa = matrix(m_aa)
        cov_aa = matrix(cov_aa)
        gauss_aa = {'m': m_aa, 'cov': cov_aa}
        
        m_ab = np.mean(self.pab, axis=0)
        cov_ab = np.cov(np.array(self.pab).T)
        m_ab = matrix(m_ab)
        cov_ab = matrix(cov_ab)
        gauss_ab = {'m': m_ab, 'cov': cov_ab}
        
        m_bb = np.mean(self.pbb, axis=0)
        cov_bb = np.cov(np.array(self.pbb).T)
        m_bb = matrix(m_bb)
        cov_bb = matrix(cov_bb)
        gauss_bb = {'m': m_bb, 'cov': cov_bb}
        
        self.gauss_params = {'aa': gauss_aa, 'ab': gauss_ab, 'bb': gauss_bb}
    
    # return gaussian parameters
    def get_gauss_params(self):
        return self.gauss_params

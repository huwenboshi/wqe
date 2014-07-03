from cvxopt import matrix
import numpy as np
import time
import math

# caller for socal using ellipsoidal separation
class gauss_caller:

    # initialize the genotype_trainer
    def __init__(self, m_aa, cov_aa, m_ab, cov_ab, m_bb, cov_bb):
        self.m_aa = m_aa
        self.cov_aa = cov_aa
        self.m_ab = m_ab
        self.cov_ab = cov_ab
        self.m_bb = m_bb
        self.cov_bb = cov_bb
    
    # mahalanobis distance
    def mindist(self, x):
        min_dist = None
        score = None
        genotype = None
        
        # compute distance to aa
        c_aa = self.m_aa
        E_aa = self.cov_aa
        
        val = ((x-c_aa).trans()*E_aa*(x-c_aa))[0]
        if(val < 0):
            val = 0
        dist_aa = math.sqrt(val)
        min_dist = dist_aa
        genotype = 'aa'
        
        # compute distance to ab
        c_ab = self.m_ab
        E_ab = self.cov_ab
        val = ((x-c_ab).trans()*E_ab*(x-c_ab))[0]
        if(val < 0):
            val = 0
        dist_ab = math.sqrt(val)
        if(dist_ab < min_dist):
            min_dist = dist_ab
            genotype = 'ab'
        
        # compute distance to bb
        c_bb = self.m_bb
        E_bb = self.cov_bb
        val = ((x-c_bb).trans()*E_bb*(x-c_bb))[0]
        if(val < 0):
            val = 0
        dist_bb = math.sqrt(val)
        if(dist_bb < min_dist):
            min_dist = dist_bb
            genotype = 'bb'
        
        # compute score
        score = 1-min_dist/(dist_aa+dist_ab+dist_bb)
        
        return (genotype, score)

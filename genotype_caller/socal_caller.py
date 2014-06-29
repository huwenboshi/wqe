from cvxopt import matrix
import numpy as np
import time
import math

# caller for socal using ellipsoidal separation
class socal_caller:

    # initialize the genotype_trainer
    def __init__(self, c_aa, E_aa, c_ab, E_ab, c_bb, E_bb, c4):
        self.c_aa = c_aa
        self.E_aa = E_aa/c4
        self.c_ab = c_ab
        self.E_ab = E_ab/c4
        self.c_bb = c_bb
        self.E_bb = E_bb/c4
        
    # minimum distance classifier
    def mindist(self, x):
        min_dist = None
        score = None
        genotype = None
        
        # compute distance to aa
        c_aa = self.c_aa
        E_aa = self.E_aa
        
        val = ((x-c_aa).trans()*E_aa*(x-c_aa))[0]
        if(val < 0):
            return None
        dist_aa = math.sqrt(val)
        min_dist = dist_aa
        genotype = 'aa'
        
        # compute distance to ab
        c_ab = self.c_ab
        E_ab = self.E_ab
        val = ((x-c_ab).trans()*E_ab*(x-c_ab))[0]
        if(val < 0):
            return None
        dist_ab = math.sqrt(val)
        if(dist_ab < min_dist):
            min_dist = dist_ab
            genotype = 'ab'
        
        # compute distance to bb
        c_bb = self.c_bb
        E_bb = self.E_bb
        val = ((x-c_bb).trans()*E_bb*(x-c_bb))[0]
        if(val < 0):
            return None
        dist_bb = math.sqrt(val)
        if(dist_bb < min_dist):
            min_dist = dist_bb
            genotype = 'bb'
        
        # compute score
        score = 1-min_dist/(dist_aa+dist_ab+dist_bb)
        
        """
        print c_aa
        print E_aa
        print c_ab
        print E_ab
        print c_bb
        print E_bb
        """
        
        return (genotype, score)

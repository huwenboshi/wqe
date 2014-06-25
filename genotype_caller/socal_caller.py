from cvxopt import matrix
import numpy as np
import time
import math

# caller for socal using ellipsoidal separation
class socal_caller:

    # initialize the genotype_trainer
    def __init__(self, snpid, c_aa, E_aa, c_ab, E_ab, c_bb, E_bb, c4):
        self.snpid = snpid
        self.c_aa = c_aa
        self.c_ab = c_ab
        self.c_bb = c_bb
        self.E_aa = E_aa
        self.E_ab = E_ab
        self.E_bb = E_bb
        
    # minimum distance classifier
    def mindist(self, x):
        min_dist = None
        score = None
        genotype = None
        
        # compute distance to aa
        c_aa = self.c_aa
        E_aa = self.E_aa
        dist_aa = math.sqrt(((x-c_aa).trans()*E_aa*(x-c_aa))[0])
        min_dist = dist_aa
        genotype = 'AA'
        
        # compute distance to ab
        c_ab = self.c_ab
        E_ab = self.E_ab
        dist_ab = math.sqrt(((x-c_ab).trans()*E_ab*(x-c_ab))[0])
        if(dist_ab < min_dist):
            min_dist = dist_ab
            genotype = 'AB'
        
        # compute distance to bb
        c_bb = self.c_bb
        E_bb = self.E_bb
        dist_bb = math.sqrt(((x-c_bb).trans()*E_bb*(x-c_bb))[0])
        if(dist_bb < min_dist):
            min_dist = dist_bb
            genotype = 'BB'
        
        # compute score
        score = 1-min_dist/(dist_aa+dist_ab+dist_bb)
        
        return (genotype, score)

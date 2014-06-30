from cvxopt import matrix
import numpy as np
import time
import math

# caller for socal using ellipsoidal separation
class socal_caller:

    # initialize the genotype_trainer
    def __init__(self, c_aa, E_aa, c_ab, E_ab, c_bb, E_bb, c4,
                 aa_state, ab_state, bb_state):
        self.aa_state = aa_state
        self.ab_state = ab_state
        self.bb_state = bb_state
        self.c_aa = None
        self.E_aa = None
        self.c_ab = None
        self.E_ab = None
        self.c_bb = None
        self.E_bb = None        
        if(self.aa_state != None):
            self.c_aa = c_aa
            self.E_aa = E_aa/c4
        if(self.ab_state != None):
            self.c_ab = c_ab
            self.E_ab = E_ab/c4
        if(self.bb_state != None):
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
        
        if(self.aa_state != None and self.aa_state != None):
            val = ((x-c_aa).trans()*E_aa*(x-c_aa))[0]
            if(val < 0):
                val = 0
            dist_aa = math.sqrt(val)
        else:
            dist_aa = 9999999999.0
        min_dist = dist_aa
        genotype = 'aa'
        
        # compute distance to ab
        c_ab = self.c_ab
        E_ab = self.E_ab
        if(self.ab_state != None and self.ab_state != None):
            val = ((x-c_ab).trans()*E_ab*(x-c_ab))[0]
            if(val < 0):
                val = 0
            dist_ab = math.sqrt(val)
        else:
            dist_ab = 9999999999.0
        if(dist_ab < min_dist):
            min_dist = dist_ab
            genotype = 'ab'
        
        # compute distance to bb
        c_bb = self.c_bb
        E_bb = self.E_bb
        if(self.bb_state != None and self.bb_state != None):
            val = ((x-c_bb).trans()*E_bb*(x-c_bb))[0]
            if(val < 0):
                val = 0
            dist_bb = math.sqrt(val)
        else:
            dist_bb = 9999999999.0
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

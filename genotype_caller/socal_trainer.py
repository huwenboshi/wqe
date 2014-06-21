from maxsep import *
from robsep import *

# trainer for socal using ellipsoidal separation
class socal_trainer:
    
    # initialize the genotype_caller, using robsep
    def __init__(self, snpid, paa, pab, pbb, c1, c2, c3):
        self.snpid = snpid
        self.paa = paa
        self.pab = pab
        self.pbb = pbb
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.sep = robsep()
        self.sep.set_param(c1, c2, c3)
    
    # train the socal genotype caller - find ellipsoidal separator
    def train(self):
    
        # find ellipsoid containing aa
        aa = self.paa
        non_aa = self.pab+self.pbb
        self.sep.set_data(aa, non_aa)
        e_aa = self.sep.find_ellipsoid()
        
        # find ellipsoid containing ab
        ab = self.pab
        non_ab = self.paa+self.pbb
        self.sep.set_data(ab, non_ab)
        e_ab = self.sep.find_ellipsoid()
        
        # find ellipsoid containing bb
        bb = self.pbb
        non_bb = self.paa+self.pab
        self.sep.set_data(bb, non_bb)
        e_bb = self.sep.find_ellipsoid()
        
        self.ellipsoids = {'aa': e_aa, 'ab': e_ab, 'bb': e_bb}

    # get the ellipsoids
    def get_ellipsoids():
        return self.ellipsoids

    # rescure missing cluster
    def rescue(self):
    
        # count the number of missing clusters
        nmiss = 0
        if(self.ellipsoids['aa'] == None):
            nmiss = nmiss+1
        if(self.ellipsoids['ab'] == None):
            nmiss = nmiss+1
        if(self.ellipsoids['bb'] == None):
            nmiss = nmiss+1
        
        # cannot rescure under the following situations
        # 2 or more clusters are missing
        if(nmiss >= 2):
            return
        # the ab genotype cluster is missing
        if(self.ellipsoids['ab'] == None):
            return
        
        # rescue the following situations
        # aa cluster missing
        if(self.ellipsoids['aa'] == None):
            # rescure using bb cluster and ab cluster
            return
        
        # bb cluster missing
        if(self.ellipsoids['bb'] == None):
            # rescure using aa cluster and ab cluster
            return

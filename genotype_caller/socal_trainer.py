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
        (c1, E1, rho1) = self.sep.find_ellipsoid()
        print c1
        
        # find ellipsoid containing ab
        ab = self.pab
        non_ab = self.paa+self.pbb
        self.sep.set_data(ab, non_ab)
        # (c2, E2, rho2) = self.sep.find_ellipsoid()
        # print c2
        
        # find ellipsoid containing bb
        bb = self.pbb
        non_bb = self.paa+self.pab
        self.sep.set_data(bb, non_bb)
        (c3, E3, rho3) = self.sep.find_ellipsoid()
        print c3

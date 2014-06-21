from maxsep import *
from robsep import *

# trainer for socal using ellipsoidal separation
class socal_trainer:
    
    # initialize the genotype_caller, using maxsep
    def __init__(self, snpid, paa, pab, pbb):
        self.paa = paa
        self.pab = pab
        self.pbb = pbb
        self.sep = 'maxsep'
    
    # initialize the genotype_caller, using robsep
    def __init__(self, snpid, paa, pab, pbb, c1, c2, c3):
        self.paa = paa
        self.pab = pab
        self.pbb = pbb
        self.sep = 'robsep'

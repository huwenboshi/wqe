from maxsep import *
from robsep import *
from utils import *
import numpy as np

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
        
        # rescue the following situations
        # aa cluster missing
        if(self.ellipsoids['aa'] == None):
        
            # rescure using bb cluster and ab cluster
            e_bb = self.ellipsoids['bb']
            e_ab = self.ellipsoids['ab']
            
            # initialize
            e_aa = dict()
            
            # get ellipsoids' orientation
            (u_bb, s_bb, v_bb) = np.linalg.svd(e_bb['E'])
            major_bb_vec = u_bb[:,1]
            (u_ab, s_ab, v_ab) = np.linalg.svd(e_ab['E'])
            major_ab_vec = u_ab[:,1]
            ang_bb_ab = angle(major_bb_vec, major_ab_vec)
            
            # estimate center
            major_ab_vec_u = get_unit_vec(major_ab_vec)
            e_bb_c = e_bb['c']
            e_ab_c = e_ab['c']
            e_aa_c = -e_bb_c+2*e_ab_c
            scalar = 2*np.dot((e_bb_c-e_ab_c).trans(),major_ab_vec_u)
            e_aa_c += scalar*major_ab_vec_u
            e_aa['c'] = matrix(e_aa_c)
            
            # copy the ab ellipsoid to aa
            rot_ab_mat = rot_mat(-ang_bb_ab)
            e_aa['E'] = e_ab['E']*rot_ab_mat
            e_aa['rho'] = e_ab['rho']
            
            # save the rescue
            self.ellipsoids['aa'] = e_aa
            
            return
        
        # ab cluster missing
        if(self.ellipsoids['ab'] == None):
            
            # rescure using aa cluster and bb cluster
            e_aa = self.ellipsoids['aa']
            e_bb = self.ellipsoids['bb']
            
            # initialize
            e_ab = dict()
            
            # estimate center
            e_ab['c'] = (e_aa['c']+e_bb['c'])/2.0
            
            # get ellipsoids' orientation
            (u_aa, s_aa, v_aa) = np.linalg.svd(e_aa['E'])
            major_aa_vec = u_aa[:,1]
            (u_bb, s_bb, v_bb) = np.linalg.svd(e_bb['E'])
            major_bb_vec = u_bb[:,1]
            ang_aa_bb = angle(major_aa_vec, major_bb_vec)
            ang_aa_bb_half = ang_aa_bb/2
            
            # copy the ellipsoid with smaller major axis length
            major_aa_len = 1/math.sqrt(s_aa[1])
            major_bb_len = 1/math.sqrt(s_bb[1])
            if(major_aa_len <= major_bb_len):
                rot_aa_mat = rot_mat(ang_aa_bb_half)
                e_ab['E'] = e_aa['E']*rot_aa_mat
                e_ab['rho'] = e_aa['rho']
            else:
                rot_aa_mat = rot_mat(-ang_aa_bb_half)
                e_ab['E'] = e_bb['E']*rot_bb_mat
                e_ab['rho'] = e_bb['rho']
            
            # save the rescue
            self.ellipsoids['ab'] = e_ab
            
            return
        
        # bb cluster missing
        if(self.ellipsoids['bb'] == None):
            # rescure using aa cluster and ab cluster
            return

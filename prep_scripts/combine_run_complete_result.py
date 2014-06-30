#!/usr/bin/python

from optparse import OptionParser
import sys
import math
import time

# get command line
parser = OptionParser()
parser.add_option("-p", "--prefix", dest="prefix")
parser.add_option("-l", "--lower", dest="lower")
parser.add_option("-u", "--upper", dest="upper")

(options, args) = parser.parse_args()

prefix_nm = options.prefix
lower_nm = options.lower
upper_nm = options.upper

# check command line
if(prefix_nm == None or lower_nm == None or upper_nm == None):
    sys.stderr.write("Usage:\n")
    sys.stderr.write("\tUse -p to specify prefix\n")
    sys.stderr.write("\tUse -l to specify lower\n")
    sys.stderr.write("\tUse -u to specify upper\n")
    sys.exit()
    
lower = int(lower_nm)
upper = int(upper_nm)

fcall_combined = open(prefix_nm+'_call_combined.txt', 'w')
fconf_combined = open(prefix_nm+'_conf_combined.txt', 'w')
for i in xrange(lower, upper+1):
    fcall = open(prefix_nm+'.'+str(i)+'_call.txt', 'r')
    fconf = open(prefix_nm+'.'+str(i)+'_conf.txt', 'r')
    if(i == lower):
        for line in fcall:
            line = line.strip()
            fcall_combined.write(line+'\n')
        for line in fconf:
            line = line.strip()
            fconf_combined.write(line+'\n')
    else:
        flr = False
        for line in fcall:
            line = line.strip()
            if(flr == False):
                flr = True
                continue
            fcall_combined.write(line+'\n')
        flr = False
        for line in fconf:
            line = line.strip()
            if(flr == False):
                flr = True
                continue
            fconf_combined.write(line+'\n')
    fcall.close()
    fconf.close()
    
fcall_combined.close()
fconf_combined.close()

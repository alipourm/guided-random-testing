import os
import sys
import re
import pickle
import numpy as np
import glob

targets_conf = {}

def jsfilecount(dir):
	return len(glob.glob(os.path.join(dir,  '*.js')))

def cfgexists(dir):
	return len(glob.glob(os.path.join(dir, '*cfg'))) > 0	

def get_targets(f):
    loglines = open(f).readlines()
#    print loglines
    limits = []
    new_target = False
    for i, l in enumerate(loglines):   
        # print l
        if 'Director:' in l:
            limits.append(i)



    for i in range(len(limits)):
#        print i, len(limits)
      
        low = limits[i]
        if i == len(limits) - 1:
            high = len(loglines)
        else:
            high = limits[i + 1]
        ls = loglines[low:high]
        directory = ls[0].strip().split(':')[-1]
        target = int(ls[1].strip().split(':')[-1])
        data_num =  int(re.findall('replica(\d+)', directory)[0]) - 1
        # print directory
        directory = '/scratch/alipour/data/' + str(data_num) +  '/'.join(directory.split('/')[-3:])
        basedata = '/'.join(directory.split('/')[:-2]) + '/init' 
        base = np.load(basedata + '/linecov.npy')
        covdata = os.path.join(directory, 'linecov.npy')
        # print covdata
        d = np.load(open(covdata))
        if 'no_swarm' in directory:
            tech = 'no_swarm'
        if 'half_swarm' in directory:
            tech = 'halfswarm'
        # print d
        if d.size != 0:
		dd = d[target]
	else:
		dd = 0

	print '{0}, {1}, {2}, {3}, {4},{5},{6},{7}, {8}'.format(tech,  dd, jsfilecount(directory), cfgexists(directory) , base[target], jsfilecount(basedata),  directory, basedata, target)
        

            
            



def scan_logs(dir):
    for root, dirs, files in os.walk(dir):
        if 'guided-test-debug.log' in files:
           get_targets(os.path.join(root, 'guided-test-debug.log'))
           

def lookforduplicateconf(dir):
    d = []
    for root, dirs, files in os.walk(dir):
        if 'target.cfg' in files:
            print root
            c = open(os.path.join(root, 'target.cfg')).read()
            d.append(c)
    print len(d), len(set(d))

#lookforduplicateconf(sys.argv[1])
get_targets(sys.argv[1])
# print targets_conf

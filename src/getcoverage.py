import glob
import numpy as np
import sys
import os
coverage_file = sys.argv[1]

cwd = os.getcwd()
info = []

print "directory,target,hitrate,randomhitrate,swarmrate"

for line in open(coverage_file).readlines():
    l = line.strip()
    directory, target_str = l.split(',')
    os.chdir(directory)
    target = int(target_str)

    
    npyfiles = glob.glob("*npy")
    if len(npyfiles) == 0:
        continue
    npy = npyfiles[0]
    p = np.load(open(npy))
    try:
        hitrate =  float(p[target])/max(p)
        info.append((directory, target, hitrate))
    except IndexError:
        pass
    

    os.chdir(cwd)
    

for directory, target, hitrate in info:
    dirparts = directory.split(os.sep)
    randomparts = dirparts[:-2] + ["random"]
    randomdir = '/'.join(randomparts)

    try:
        os.chdir(randomdir)
    except OSError:
        continue
        
    npyfiles = glob.glob("*npy")
    if len(npyfiles) == 0:
        continue
    npy = npyfiles[0]
    p = np.load(open(npy))
    try:
        randomhitrate =  float(p[target])/max(p)
#        print "{0},{1},{2},{3}".format(directory, target, hitrate, randomhitrate)
    except IndexError:
        continue

    initparts = dirparts[:-2] + ["init"]
    randomdir = '/'.join(initparts)
    
    try:
        os.chdir(randomdir)
    except OSError:
        continue
        
    npyfiles = glob.glob("*npy")
    if len(npyfiles) == 0:
        continue
    npy = npyfiles[0]
    p = np.load(open(npy))
    try:
        swarmrate =  float(p[target])/max(p)
        print "{0},{1},{2},{3},{4}".format(directory, target, hitrate, randomhitrate, swarmrate)
    except IndexError:
        pass

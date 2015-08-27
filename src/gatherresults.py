import glob
import sys
import os
import numpy as np
import re

logfile_list =  map(lambda s: s.strip(), open(sys.argv[1]).readlines())
if sys.argv[2] == 'js':
    postfix = '*.js'
else:
    postfix = '*.c'



initcov = np.array([])
origtsize = 0

def getMode(direcotry):
    if 'greedy' in directory:
        return "Greedy"
    if 'round' in directory:
        return "Round-robin"
    if 'ressive' in directory:
        return "Aggressive"

print '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}'.format('directory', 'mode',  'beforemerge','target', 'newcov',  'initcov', 'tsize', 'origtsize', 'initratio', 'newratio', 'Mode')

for logfile in logfile_list:
    for line in open(logfile):
        # print line
        if 'init' in line and 'Directory' in line:
            
            line = line.strip()
            initdir = re.findall('Directory:(.*) ', line)[0]
            initcovfile = os.path.join(initdir, 'covsummary.npy')
            initcov = np.load(initcovfile)
            origtsize = re.findall('TSSIZE:(\d+)', line)[0]

      #      print initcov.size
        if 'Directory:' in line and 'Target:' in line:
            # print line
            lparts = line.split()
            for part in lparts:
                if part.startswith('Directory'):
                    directory = part.replace('Directory:', '')
                    tsize = re.findall('TSSIZE:(\d+)', line)[0]
                    if tsize == 0:
                       tsize = initcov.max()
            # infopart = line.strip().split('-')[6]
       #     print infopart
            targets = re.findall('Target:(\[.*\]), ', line)
            targets = eval(targets[0])

                            

            merge = re.findall('BeforeMerge:(\d+), ', line)[0]            
            covfile = os.path.join(directory, 'covsummary.npy')
        #    print 'directory', covfile
            try:
                coverage = np.load(covfile)
                if len(coverage) == 0:
                    continue
                tot_initratio = 0
                tot_newratio = 0
		for target in targets:                
			initratio = initcov[target]/ float(origtsize)
			newratio = coverage[target]/float(tsize)
                        tot_initratio += initratio
                        tot_newratio += newratio
                initratio = tot_initratio / len(targets)
                newratio = tot_newratio/ len(targets)
# 'directory', 'InclusionMode', 'Features', 'beforemerge','target', 'newcov',  'initcov', 'tsize', 'origtsize', 'initratio', 'newratio', 'MergeMode'
                aftermerge=re.findall('AfterMerge:(\d+),', line)[0]
                print '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}'.format(directory,
                                                                                  directory.split(os.sep)[-1],
                                                                                  merge, len(targets),
                                                                                  coverage[target], initcov[target], tsize,
                                                                                  origtsize, initratio, newratio,
                                                                                  getMode(directory))

            except IOError, IndexError:
                pass
            


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

print '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}'.format('directory', 'treatment', 'merge', 'targetlen','target', 'newcov',  'initcov', 'tsize', 'origtsize', 'initratio', 'newratio')

for logfile in logfile_list:
    for line in open(logfile):
        if 'init' in line:
            initdir = line.strip().split()[-1]
            initcovfile = os.path.join(initdir, 'covsummary.npy')
            initcov = np.load(initcovfile)
            origtsize = len(glob.glob(os.path.join(initdir, postfix)))
            if origtsize == 0:
                origtsize = initcov.max()
      #      print initcov.size
        if 'Directory:' in line and 'Target:' in line:
            # print line
            lparts = line.split()
            for part in lparts:
                if part.startswith('Directory'):
                    directory = part.replace('Directory:', '')
                    tsize = len(glob.glob(os.path.join(directory, postfix)))
                    if tsize == 0:
                       tsize = initcov.max()
            # infopart = line.strip().split('-')[6]
       #     print infopart
            targets = re.findall('Target:(\[.*\])', line)
            if len(targets) != 0:
                targets = eval(targets[0])
            else:
                targets = [eval(re.findall('Target:(\d+) Mode', line)[0])]
                            

            merge = re.findall('Merge:(.*)', line)[0]            
            covfile = os.path.join(directory, 'covsummary.npy')
        #    print 'directory', covfile
            try:
                coverage = np.load(covfile)
                if len(coverage) == 0:
                    continue
		for target in targets:                
			initratio = initcov[target]/ float(origtsize)
			newratio = coverage[target]/float(tsize)
			print '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}'.format(directory, directory.split(os.sep)[-1], merge, len(targets), target, coverage[target],  initcov[target], tsize, origtsize, initratio, newratio)

            except IOError, IndexError:
                pass
            


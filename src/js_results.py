import glob
import sys
import os
import numpy as np


logfile_list =  glob.glob(sys.argv[1])




initcov = np.array([])
origtsize = 0
for logfile in logfile_list:
    for line in open(logfile):
        if 'init' in line:
            initdir = line.strip().split()[-1]
            initcovfile = os.path.join(initdir, 'covsummary.npy')
            initcov = np.load(initcovfile)
            origtsize = len(glob.glob(os.path.join(initdir, "*.js")))
        # print initcov.size
        if 'Directory:' in line and 'Target:' in line:
            lparts = line.split()
            for part in lparts:
                if part.startswith('Directory'):
                    directory = part.replace('Directory:', '')
                    tsize = len(glob.glob(os.path.join(directory, "*.js")))
                if part.startswith('Target'):
                    target = int(part.replace('Target:', ''))
            covfile = os.path.join(directory, 'covsummary.npy')
            try:
                coverage = np.load(covfile)[target]
                print '{0},{1},{2},{3},{4},{5},{6}'.format(directory, directory.split(os.sep)[-1], target, coverage,  initcov[target], tsize, origtsize)

            except Exception:
                pass
            


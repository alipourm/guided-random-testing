import os
import numpy as np
import pandas as pd
import pickle
import sys
# average coverage per line
# average coverage
# covering new stuff
# finding new bugs


COVERAGEFILENAMES = 'COVERAGEFILENAMES'

def getExperimentMicroNumber(tcpath):
    if 'init' in tcpath:
        return -1
    tcpathparts = tcpath.split(os.sep)
    return int(tcpathparts[-1])


def getSelectionMethod(tcpath):
    if 'init' in tcpath:
        return 'init'
    tcpathparts = tcpath.split(os.sep)
#    print tcpath
    return tcpathparts[-2]

def getExperimentMacroNumber(tcpath):
     tcpathparts = tcpath.split(os.sep)
     if 'init' in tcpath:
        return int(tcpathparts[-2])
     return int(tcpathparts[-3])


# Note when we use dataframe we lose flexibility a lot by hardcoding
# a lot of logic in data.
import glob 
data_frames = []
for f in glob.glob('*.df'):
	data_frames.append(pd.read_pickle(f))

df = pd.concat(data_frames)
df['tcpath'] = df.index.copy()	

df['is_seed'] = df['tcpath'].apply(lambda tcpath: True if 'init' in tcpath else False)

df['selection_method'] = df['tcpath'].apply(getSelectionMethod)
df['experimentno_macro'] = df['tcpath'].apply(getExperimentMacroNumber)
df['experimentno_micro'] = df['tcpath'].apply(getExperimentMicroNumber)

df['baseline'] = df['tcpath'].apply(lambda s: s if 'init' in s else '/'.join(s.split('/')[:-2] + ['init']))


selection_methods = df.selection_method.unique()
experiments = df.experimentno_macro.unique()
coverages = ['linecov.npy', 'branchcov.npy']

def tobinary(n):
    if n > 0:
        return 1
    else:
        return 0


vtobinary = np.vectorize(tobinary)
                    
print '{0},{1},{2}, {3}, {4}'.format('experiment', 'selection', 'coverage', 'coverage.extra', 'coverage.less')

for e in experiments:
	for s in selection_methods:
            if s == 'init':
                continue
            td = df[df['experimentno_macro'] == e]
            base = td[td['is_seed'] == True]
            d = td[td['selection_method'] == s]

            for c in coverages:
                basecov = base[c].values[0]
                basebin = vtobinary(basecov)
                cc2  = d[c].apply(lambda x:vtobinary(x))
                for cc in cc2.values:
                   diff = cc - basebin
                   extranum = np.extract(diff == 1, diff).size
                   lessnum = np.extract(diff == -1, diff).size
                   print '{0},{1},{2}, {3}, {4}'.format(e, s, c, str(extranum), int(lessnum))

                
                
                
		
		 			


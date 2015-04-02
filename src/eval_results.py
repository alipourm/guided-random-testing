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

#df['brdiff'] = df['branchcov.npy'] - df.loc[df['baseline']]['branchcov.npy']
newdfs = [df[df[experimentno_macro] > 5],  df[df[experimentno_macro] <= 5]] 
groupings = []
for df in newdfs:
    groupings.append(df.groupby(['experimentno_macro', 'selection_method']))

exp = []
for g in groupings:
	k = g['branchcov.npy'].agg({'sum': np.sum, 'average': np.avarage})
	exp.append(k)
def addarrays(df):
	result = df.iloc[0]
	for i in range(1, len(df)):
		result += df.iloc[1]
	return result


selection_methods = df.selection_method.unique()
experiments = df.experimentno_macro.unique()
coverages = ['linecov.npy', 'branchcov.npy']
for e in experiments:
	for s in selection_methods:
		td = df[df['experiments'] == e]
		base = td[td['is_seed'] == True]
		d = td[td['selection_method'] == s]
		
		 			


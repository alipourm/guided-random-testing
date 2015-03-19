import os
import numpy as np
import pandas as pd
import pickle
# average coverage per line
# average coverage
# covering new stuff
# finding new bugs


COVERAGEFILENAMES = 'COVERAGEFILENAMES'

# extract all file names
if not os.path.exists(COVERAGEFILENAMES):
    coveragefilenames = []
    for dirpath, dirnames, filenames in os.walk('../data'):
        for f in filenames:
            if f.endswith('js'):
                coveragefilenames.append(f)

    pickle.dump(coveragefilenames, open(COVERAGEFILENAMES, 'w'))
else:
    coveragefilenames = pickle.load(COVERAGEFILENAMES)

#load all data into the dataframe
df = pd.DataFrame({'tcpath': coveragefilenames})

df['is_seed'] = df['tcpath'].apply(lambda tcpath: True if 'init' in tcpath else False)

def getSelectionMethod(tcpath):
    if 'init' in tcpath:
        return 'init'
    tcpathparts = tcpath.split(os.sep)
    return tcpathparts[-2]

def getExperimentNumber(tcpath):
    if 'init' in tcpath:
        return -1
    tcpathparts = tcpath.split(os.sep)
    return int(tcpathparts[-1])


def getExperimentNumber(tcpath):
    if 'init' in tcpath:
        return -1
    tcpathparts = tcpath.split(os.sep)
    return int(tcpathparts[-3])


df['slection_method'] = df['tcname'].apply(getSelectionMethod)
df['experimentno']


df['lcov'] = df['tcpath'].apply(lambda tcpath: np.array(pickle.load(open(tcpath + '.lcov'))))
df['bcov'] = df['tcpath'].apply(lambda tcpath: np.array(pickle.load(open(tcpath + '.bcov'))))
df['fncov'] = df['tcpath'].apply(lambda tcpath: np.array(pickle.load(open(tcpath + '.fncov'))))




        

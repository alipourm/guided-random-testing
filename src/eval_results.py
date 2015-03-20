import os
import numpy as np
import pandas as pd
import pickle
# average coverage per line
# average coverage
# covering new stuff
# finding new bugs


COVERAGEFILENAMES = 'COVERAGEFILENAMES'

def getExperimentMicroNumber(tcpath):
    if 'init' in tcpath:
        return -1
    tcpathparts = tcpath.split(os.sep)
    return int(tcpathparts[-2])


def getSelectionMethod(tcpath):
    if 'init' in tcpath:
        return 'init'
    tcpathparts = tcpath.split(os.sep)
    print tcpath
    return tcpathparts[-3]

def getExperimentMacroNumber(tcpath):
    if 'init' in tcpath:
        return -1
    tcpathparts = tcpath.split(os.sep)
    return int(tcpathparts[-4])



def load(filename):
    try:
        f = open(filename)
        return np.array(pickle.load(f))
    except IOError:
        return np.array([]) # for non-terminating test cases returns an empty array



# extract all file names
if not os.path.exists(COVERAGEFILENAMES):
    coveragefilenames = []
    for dirpath, dirnames, filenames in os.walk('data'):
        for f in filenames:
            print f
            if f.endswith('js'):
                coveragefilenames.append(os.path.join(dirpath,f))

    pickle.dump(coveragefilenames, open(COVERAGEFILENAMES, 'w'))
    
else:
    coveragefilenames = pickle.load(open(COVERAGEFILENAMES))

#load all data into the dataframe
df = pd.DataFrame({'tcpath': coveragefilenames})

df['is_seed'] = df['tcpath'].apply(lambda tcpath: True if 'init' in tcpath else False)

df['slection_method'] = df['tcpath'].apply(getSelectionMethod)
df['experimentno_macro'] = df['tcpath'].apply(getExperimentMacroNumber)
df['experimentno_micro'] = df['tcpath'].apply(getExperimentMicroNumber)

df['lcov'] = df['tcpath'].apply(lambda tcpath: load(tcpath + '.lcov'))
df['bcov'] = df['tcpath'].apply(lambda tcpath:load(tcpath + '.bcov'))
df['fcov'] = df['tcpath'].apply(lambda tcpath:load(tcpath + '.fncov'))


df.to_csv('COVERAGES.CSV')


        

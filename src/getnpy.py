import numpy as np
import sys
import glob


lcovfiles = glob.glob(sys.argv[1])



# 2015-05-13 08:21:10,135 - GCC - INFO - Directory:/scratch/gcc_data/1/roundroubin.0.20/halfswarm Target:[155360, 54662, 129910, 181685, 258542, 67901, 131393, 57271, 157830, 134337, 129929, 269337, 259737, 125008, 42377, 52972, 256878, 290643, 28086, 193271], Mode:halfswarm, Merge:roundrobin_merge, BeforeMerge:20, AfterMerge:20, TSSIZE:39

targets = [155360, 54662, 129910, 181685, 258542, 67901, 131393, 57271, 157830, 134337, 129929, 269337, 259737, 125008, 42377, 52972, 256878, 290643, 28086, 193271]




def summarize(kk):
    l = []
    for lcov in lcovfiles:
        print lcov
        dat = np.load(open(lcov))
        l.append(dat)

    k = np.sum(l, axis=0)
    print k
    print type(k)
    np.save(open("covsummary.npy",'w'), k)

def loaddata(f):
    return np.load(f)


def main():
    total = 0
    summarize(lcovfiles)
    d = loaddata("covsummary.npy")
    print d
    d= d/float(max(d))
    for t in targets:
        print d[t]
        total += d[t]

    print total/len(targets)

main()
        
        
        

import sys
import os
import numpy as np
from scipy.spatial import distance
import pandas as pd
import itertools


def getcsvfiles(files):
    dataframes = []
    for f in files:
        print 'Loading {0} ...'.format(f)
        dataframes.append(pd.DataFrame.from_csv(f))
    return dataframes


def getbitvectors(tr):
    result = set()
    for (bv, length, lines) in tr:
        result.add(bv)
    return result

def join(df1, df2):
    pass

def interaction(df):
    pass

def ischange(l):
    pass

def changes(df):
    pass





#def numberof bitvectors()
#intersection union



def getfiles(logfiledir):
    logfile_list = []
    for fn in open(logfiledir):
#        print fn
        logfile_list.append(fn.strip())
    return logfile_list


def getrelations(df):
    featrel  = []
    for col in df.columns:
        if 'relation' in col:
            featrel.append(col)

    return sorted(featrel)



def groupstats(df, featrel):
    df['lineno'] = df.index.copy()
    gr = df.groupby(featrel)
    rels = []
    for name, group in gr:
         rels.append((name,len(group), group['lineno'].values))
    return rels



def getdf(fn):
    return pd.DataFrame.from_csv(fn)








def subsumes(rel1, rel2):
    for n in range(len(rel1)):
        i = rel1[n]
        j = rel2[n]
        if i != j:
            if j != 'I':
                return False
    return True


def compatiblepartitions(rels):
    res = {}
    for i, rel1 in enumerate(rels):
        for j, rel2 in enumerate(rels):
            if i != j and subsumes(rel1, rel2):
                res[(i,j)] = True
#                print '{0}->{1}'.format(i,j)
    return res
        



def otherpathexisst(i,j, res):
    for (k,l) in res:
        if k != j and l != j and res[(k,l)]:
            if (i,k) in res:
                if (k,j) in res:
                    if res[(i,k)] and res[(k,j)]:
                        return True
    return False


def prune(res):
    for n in res:
        if res[n] and otherpathexisst(n[0], n[1],res):
#            print "inv"
            res[n] = False
    return res
        


def intersect(frdict):
    intersectset = set()
    firsttime = True
    for f in frdict:
        fset = getbitvectors(frdict[f])
        print len(fset)
        if firsttime:
            intersectset = fset.copy()
            
            firsttime = False
        else:
            intersectset = intersectset.intersection(fset)
    print intersectset, len(intersectset)
        


def getlinefeature(tripletlist):
    result = {}
    for (bv, length, lines) in tripletlist:
        for l in lines:
            result[l] = bv
    return result


def isconsistent(f, other):
    for i in range(len(f)):
        if (f[i] == 'S' and other[i] == 'T') or  (f[i] == 'T' and other[i] == 'S'):
            return False
    return True

def isgreater(f, other):
    for i in range(len(f)):
        if (f[i] == 'I' and other[i] != 'I'):
            return False
    return True

        


def conflictsperline(frdict):
    firsttime = True
    linebv = {}
    inconsistencycounter = {}
    for f in frdict:
        curlinebv = getlinefeature(frdict[f])
        if firsttime:
            linebv = curlinebv
            firsttime = False
        else:
            for l in linebv:
                if isconsistent(linebv[l], curlinebv[l]):
                    if isgreater(curlinebv[l], linebv[l]):
                        linebv[l] = curlinebv
                else:
                    if l not in inconsistencycounter:
                        inconsistencycounter[l] = 1
                    else:
                        inconsistencycounter[l] += 1
    print inconsistencycounter, len(inconsistencycounter)


def main():
    files = getfiles(sys.argv[1])
    dataframes = {}

    for f in files:
        df = getdf(f)
        dataframes[f] = df
    relations = getrelations(df)
    featrel = {}
    for f in files:
        featrel[f] = groupstats(dataframes[f], relations)

    conflictsperline(featrel)

#    intersect(featrel)
#    union(featrel)
#    inconsistentlines(featrel)
"""
    res = compatiblepartitions(featrel)
    print "starting"
    res2 = prune(res)
    for (i,j) in res2:
        if  res2[(i,j)]:
            print '{0}->{1}'.format(i,j)
    
"""

main()

import sys
import random
from z3 import *
import time

infile = sys.argv[1]

startT = time.time()

vectors = []

def matches(v1,v2):
    for i in xrange(0,len(v1)):
        if v1[i] != v2[i]:
            if (v1[i] != '2') and (v2[i] != '2'):
                return False
    return True

def subsumes(v1,v2):
    for i in xrange(0,len(v1)):
        if (v1[i] != v2[i]):
            if (v2[i] != '2'):
                return False
    return True

def merge(v1, v2):
    # Assumes can merge
    nv = ""
    for i in xrange(0,len(v1)):
        b = v1[i]
        if v2[i] < v1[i]:
            b = v2[i]
        nv += b
    return nv


for l in open(infile):
    v = l
    if v[-1] == "\n":
        v = v[:-1]
    v = v.replace('*','2')
    vectors.append(v)
    
changed = True
while changed:
    changed = False
    for i in xrange(0,len(vectors)):
        v1 = vectors[i]
        newvectors = vectors[:i+1]
        for j in xrange(i+1,len(vectors)):
            v2 = vectors[j]
            if not subsumes(v1,v2):
                newvectors.append(v2)
            else:
                print "Auto-merging vectors:",v1,v2
        if len(newvectors) < len(vectors):
            changed = True
            break
    if changed:
        vectors = newvectors

print "Done merging"
print len(vectors)

matchCount = 0 
for v1 in vectors:
    for v2 in vectors:
        if matches(v1, v2):
            matchCount += 1

print "POSSIBLE MATCHES:",(matchCount/2)

visited = {}
best = len(vectors)

def flatten(vecs):
    if vecs == []:
        return ""
    else:
        return vecs[0] + "," + flatten(vecs[1:])

def matchV(i,j):
    return Int('m' + str(i) + "." + str(j))

def vecV(i,j):
    return Int('v' + str(i) + "." + str(j))

def solveProblem(target):
    matchSet = []
    print "SOLVING WITH TARGET",target
    sys.stdout.flush()
    s = Solver()
    for i in xrange(0,len(vectors)):
        for j in xrange(0,len(vectors[i])):
                s.add(vecV(i,j) == str(vectors[i][j]))
    mSums = []
    for i in xrange(0,len(vectors)):
        for j in xrange(0,len(vectors)):
            for k in xrange(0,len(vectors[j])):
                s.add(Implies(matchV(i,j) == 1,Not(And(vecV(i,k) == 0, vecV(j,k) == 1))))
            s.add(Or(matchV(i,j) == 1, matchV(i,j) == 0))
            mSums.append(matchV(i,j))
            if (i != j):
                for k in xrange(0,len(vectors)):
                    if (k != i) and (k != j):
                        s.add(Implies(And(matchV(i,j) == 1,matchV(j,k) == 1),matchV(i,k) == 1))            
            if i < j:
                s.add(matchV(i,j) == matchV(j,i))
            elif i == j:
                s.add(matchV(i,j) == 1)
    s.add(Sum(mSums) > target)
    #s.add(M > target)
    ssat = s.check()
    if str(ssat) == "sat":
        print "SATISFIABLE"
        m = s.model()
#        print m
        total = 0
        for i in xrange(0,len(vectors)):
            for j in xrange(0,len(vectors)):
                e = str(m.evaluate(matchV(i,j)))
                if e == "1":
                    matchSet.append((i,j))
                    total += 1
                    if (i < j):
                        print (i,j),
        print
        print "TOTAL MATCHES:",total
        target = total
        sys.stdout.flush()
        return matchSet
    else:
        print "NOT SATISFIABLE"
        return None

done = False
low = len(vectors)
hi = matchCount

lastSolved = -1
lastSolution = []

while low < hi:
    print "low =",low,"hi =",hi
    target = (low + hi) / 2
    res = solveProblem(target)
    if res == None:
        hi = target - 1
    else:
        lastSolution = res
        lastSolved = len(res)
        low = target + 1


eqC = {}
for i in xrange(0,len(vectors)):
    found = False
    for j in xrange(0,i):
        if j in eqC:
            if i in eqC[j]:
                found = True
                continue
    if found:
        continue
    eqC[i] = [i]
    for j in xrange(i+1,len(vectors)):
        if (i,j) in lastSolution:
            eqC[i].append(j)

for i in eqC:
    print i,eqC[i]
    vcurr = vectors[i]
    for j in eqC[i]:
        v = vectors[j]
        if not (matches(vcurr,v)):
            print v
            print vcurr
            print "DOESN'T MATCH!"
            assert(False)
        vcurr = merge(vcurr,v)
    print vcurr
    
elapsed = time.time() - startT
print "TOTAL ELAPSED TIME",elapsed

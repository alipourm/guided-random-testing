import sys
import random
import time
import glob

infile = sys.argv[1]
tries = int(sys.argv[2])

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

possMatches = []

matchCount = 0
for i in xrange(0,len(vectors)):
    v1 = vectors[i]
    for j in xrange(0,len(vectors)):
        v2 = vectors[j]
        if matches(v1, v2):
            if i < j:
                possMatches.append((i,j))
            matchCount += 1

print "POSSIBLE MATCHES:",(matchCount/2)

visited = {}
best = len(vectors)

def flatten(vecs):
    if vecs == []:
        return ""
    else:
        return vecs[0] + "," + flatten(vecs[1:])

bestLen = len(vectors)
bestSoluton = list(vectors)

for t in xrange(0,tries):    
    random.shuffle(possMatches)

    oldVectors = list(vectors)
    
    for (i,j) in possMatches:
        v1 = vectors[i]
        v2 = vectors[j]
        if matches(v1,v2):
            merged = merge(v1,v2)
            vectors[i] = merged
            vectors[j] = merged

    sortVecs = sorted(vectors)
    solution = []
    for v in sortVecs:
        if (solution == []) or (v != solution[-1]):
            solution.append(v)
    if len(solution) < bestLen:
        bestLen = len(solution)
        print "NEW BEST SOLUTION, ON TRY",t,"OF LENGTH",bestLen
        for i, s in enumerate(solution):
            with open("new{0}.cfg".format(i), 'w') as f:
                print len(s), s
                for j, r in enumerate(s[:50]):
                    if r == '2':
                        print 'I',
                    elif r == '1': 
                        print 'T',
                    else:
                        print 'S',
    vectors = oldVectors
            
elapsed = time.time() - startT
print "TOTAL ELAPSED TIME",elapsed

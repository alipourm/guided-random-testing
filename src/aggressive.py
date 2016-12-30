__author__ = 'alipour'
import sys
import random

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

to012dict = {'S':'0',
             'T':'1',
             'I':'2'
}
toSTIdict = {'0': 'S',
             '1': 'T',
             '2': 'I'}
def to012(vector):
    return [to012dict[elem] for elem in vector]

def toSTI(vector):
    print vector
    return [toSTIdict[elem] for elem in vector]

def merge(v1, v2):
    # Assumes can merge
    nv = ""
    for i in xrange(0,len(v1)):
        b = v1[i]
        if v2[i] < v1[i]:
            b = v2[i]
        nv += b
    return nv


class Aggressive():
    def __init__(self, vectors):
        self.tries = 10000
        self.vectors = []
        for v in vectors:
            self.vectors.append(to012(v))


    def minimize(self):
        changed = True
        vectors = self.vectors
        while changed:
            changed = False

            for i in xrange(0, len(vectors)):
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


        bestLen = len(vectors)
        bestSoluton = list(vectors)

        for t in xrange(0,self.tries):
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
                #
                res = [toSTI(v) for v in solution]
                return res
            vectors = oldVectors
        return vectors

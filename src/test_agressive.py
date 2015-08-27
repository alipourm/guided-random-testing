__author__ = 'alipour'
import sys
from aggressive import *
infile = open(sys.argv[1])


vectors = []
for line in infile.readlines():
    vectors.append(line.strip())

m = Aggressive(vectors)
print len(vectors)
print len(m.minimize())

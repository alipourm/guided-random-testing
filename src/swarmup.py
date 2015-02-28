
import sys
import random
import consts

infn = sys.argv[1]
inconfn = sys.argv[2]
outfn = sys.argv[3]
outconfn = sys.argv[4]

config = open(inconfn).read().strip().split()
suppressors = [l for l in range(consts.FEATURES_MIN, consts.FEATURES_MAX+1) if ('-'+ str(l)) in config]
triggers = [l for l in range(consts.FEATURES_MIN, consts.FEATURES_MAX+1) if ('+'+  str(l)) in config]



outf = open(outfn,'w')
outcf = open(outconfn, 'w')

n = 0

for line in open(infn):
    l = line.split()
    if ((l != []) and ((l[0] == "function(dr)") or
                       (l[0] == "function(depth)")) and("}," in line)):
        n = n + 1
        if ((random.randint(0,1) == 0 or n in triggers) and n not in suppressors):
            outf.write(line)
            outcf.write("--" + str(n) + " ")
    elif ((l != []) and (l[0] == "case")):
        n = n + 1
        if (random.randint(0,1) == 0):
            outf.write(line)
            outcf.write("--" + str(n) + " ")
    else:
        outf.write(line)

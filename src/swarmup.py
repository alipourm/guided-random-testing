import sys
import random
import consts

infn = sys.argv[1]
inconfn = sys.argv[2]
outfn = sys.argv[3]
outconfn = sys.argv[4]

config = open(inconfn).read().strip().split()
potential = [l for l in range(consts.FEATURES_MIN, consts.FEATURES_MAX+1) if ('+'+ str(l)) in config]
necessary = [l for l in range(consts.FEATURES_MIN, consts.FEATURES_MAX+1) if ('++'+  str(l)) in config]



outf = open(outfn,'w')
outcf = open(outconfn, 'w')


prev = ''
feature_num = 0 


for line in open(infn):
    l = line.split()
#    line = line.strip()
    if feature_num < consts.FEATURES_MAX and ((l != []) and ((l[0] == "function(dr)") or
                       (l[0] == "function(depth)")) and("}," in line)):
        if line != prev:
            feature_num += 1
        if ((random.randint(0,1) == 0) and feature_num in potential) or (feature_num in necessary):
            outf.write(line)
            outcf.write("--" + str(feature_num) + " ")
#    elif ((l != []) and (l[0] == "case")):
#        n = n + 1
#        if (random.randint(0,1) == 0):
#            outf.write(line)
#            outcf.write("--" + str(n) + " ")
    else:
        outf.write(line)
    prev = line

import sys
import random
import JSCONSTS as consts
import re
infn = sys.argv[1]
inconfn = sys.argv[2]
outfn = sys.argv[3]
cfgfn = sys.argv[4]

config = open(inconfn).read().strip().split()
outf = open(outfn,'w')
confout = open(cfgfn,'w')
features = []
for line in open(infn):
    matches = re.findall('/\*##(\d+)##\*/', line)
    if len(matches) > 0:
        feature_num = matches[0]
        if '++'+feature_num in config:
            outf.write(line)
            features.append(feature_num)
        elif '+'+feature_num in config and random.randint(0, 1) == 0:
            outf.write(line)
            features.append(feature_num)
    else:
        outf.write(line)
# print features
confout.write(' '.join(features))
#outfn.close()

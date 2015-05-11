import sys
import random
import JSCONSTS as consts
import re
infn = sys.argv[1]
inconfn = sys.argv[2]
outfn = sys.argv[3]


config = open(inconfn).read().strip().split()
outf = open(outfn,'w')


for line in open(infn):
    matches = re.findall('/\*##(\d+)##\*/', line)
    if len(matches) > 0:
        feature_num = matches[0]
        if '++'+feature_num in config:
            outf.write(line)
        elif '+'+feature_num in config and random.randint(0, 1) == 0:
            outf.write(line)
    else:
        outf.write(line)
#outfn.close()

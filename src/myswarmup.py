import sys
import random
imoprt consts
infn = sys.argv[1]
outfn = sys.argv[2]
confn = sys.argv[3]


outf = open(outfn,'w')
outcf = open(confn, 'w')

n = 0

prev = ''
feature_num = 0 

for line in open(infn):
    l = line.split()
    line = line.strip()

    if feature_num < consts.FEATURES_MAX and ((l != []) and ((l[0] == "function(dr)") or
                       (l[0] == "function(depth)")) and("}," in line)):
        if line != prev:
            feature_num += 1

        if (random.randint(0,1) == 0):
            outf.write(line)
            outcf.write("--" + str(feature_num) + " ")

    else:
        outf.write(line)

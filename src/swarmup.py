import sys
import random
import consts


inconfn = sys.argv[1]


config = open(inconfn).read().strip().split()
potential = [l for l in range(consts.FEATURES_MIN, consts.FEATURES_MAX+1) if ('+'+ str(l)) in config]
necessary = [l for l in range(consts.FEATURES_MIN, consts.FEATURES_MAX+1) if ('++'+  str(l)) in config]
suppressors = [l for l in range(consts.FEATURES_MIN, consts.FEATURES_MAX+1) if l not in potential and l not in necessary]





prev = ''
feature_num = 0 

res = []

for line in open(inconfn):
    l = line.strip()
    feature = int(l.replace('+', ''))
    if ((random.randint(0,1) == 0) and feature in potential) or (feature in necessary):
        pass
#        res.append('--' + consts.features[int(feature)])
    else:
        res.append('--no-' + consts.features[int(feature)])

for i in suppressors:
    res.append('--no-' + consts.features[i])
print ' '.join(res)

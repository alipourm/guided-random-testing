import numpy as np
import glob
import os
import sys


for root, directories, files in os.walk(sys.argv[1]):
    if not root.endswith("random"):
        continue
    k = []
    for f in files:
        if f.endswith("cov"):
            print "root {0}, file {1}".format(root, f)
            k.append(np.load(f))

    n = sum(k)
    nf = os.path.join(root, "covsum.npy")
    print nf
    np.dump(nf)

    

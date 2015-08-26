import glob
import os
import sys


max_feature=int(sys.argv[1])
directory = sys.argv[2]

for fn in glob.glob(os.path.join(directory, "*.cfg")):
    # print "---"
    content = open(fn).read()
    for i in range(1, max_feature + 1):
        if "++{0}\n".format(i) in content:
           print "1",
        elif "+{0}\n".format(i) in content:
            print "*",
        else:
            print "0",
    print


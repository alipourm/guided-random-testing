import glob
from  coverage import *
import sys
import os

import commands 


taskid = sys.argv[1]
tclist_file = '/nfs/eecs-fserv/share/alipour/guided-random-testing-experiments/test_cases/tclist.txt'
lines = open(tclist_file).readlines()

testcases =[lines[i].strip() for i in range((int(taskid) - 1)*10, int(taskid)*10)]
spidermonkeys  = glob.glob('/nfs/eecs-fserv/share/alipour/versions.opt/js*')



for tc in testcases:
  for js in spidermonkeys:
    print js
    c = Coverage(tc)
    try:
        output = c.executetc(js)
    except InfiniteLoopError:
        output = "Infinite Loop"

    jsver = js.split(os.sep)[-1]
    outfname = tc +  '.' + jsver + '.out'
    print outfname
    outf = open(outfname, 'w')
    outf.write(output)
    outf.flush()
    outf.close()


import commands
import logging
import os
import pickle
import random
import re
import time
import glob
import logging
import sys
import numpy as np



subject = sys.argv[1]
direct = sys.argv[2]
print subject
if subject == 'gcc':
    import GCCconsts as consts
    from GCCCoverage import Coverage
    from GCCTestGen import testgen
    LOG = logging.getLogger('GCC')
    INIT_CONF = 'GCCinit.cfg'
    SEEDTESTGEN_TIME = 3600
    GUIDEDTESTGEN_TIME = 600
    tc_postfix = '.c'

elif subject == 'yaffs':
    import YAFFSConsts as consts
    from YAFFSCoverage import Coverage
    from YAFFSTestGen import testgen
    LOG = logging.getLogger('YAFFS')
    INIT_CONF = 'YAFFSinit.cfg'
    SEEDTESTGEN_TIME = 900
    GUIDEDTESTGEN_TIME = 300
    tc_postfix = '.c'
elif subject == 'js':
    import JSCONSTS as consts
    from JSCoverage import Coverage
    from JSTestGen import testgen
    import JSCONFIG as config
    LOG = logging.getLogger('JS')
    INIT_CONF = 'JSinit.cfg'
    SEEDTESTGEN_TIME = 1800
    GUIDEDTESTGEN_TIME = 600
    tc_postfix = '.js'






def run(cmd):
    # print cmd
    return commands.getstatusoutput(cmd)



first_time_coverage_calc = False
def dump_coverage(f):
    global first_time_coverage_calc
    c = Coverage(f)
    if (not first_time_coverage_calc) and subject == 'gcc':
        fname = 'coverage_map.p'
        LOG.info("Dumping coverage map at: {0}".format(fname))
        maps = c.get_mapping()
        pickle.dump(maps, open(fname, 'wb'))
        first_time_coverage_calc = True
      
    if subject == 'js':
        if 'ALL OK' not in c.output or 'ASSERT' in c.output:
            LOG.info('ASSERT in:{0}'.format(f))
            fout = open(f + '.out', 'w')
            fout.write(c.output)
            fout.close()
    # pline_cov = c.get_percent_line()
    # print line_cov
    l_cov = open(f + '.lcov', 'w')
    line_cov = c.get_l_cov()
    # LOG.info('line_cov: {0} | {1} out of {2}'.format(pline_cov, np.sum(line_cov), len(line_cov)))
    pickle.dump(line_cov, l_cov)




def generate_tests(time_length, directory, confs):
  i = 0
  start = time.time()
  # print conf
  retrycount = 0
  newi = 0
  worthy = True
  # print 'confs:', confs
  while time.time()-start < time_length and worthy and len(confs) > 0:
        print 'here'
        for conf in confs:
          if time.time()-start < time_length:
            tc_id = str(i).zfill(7)
            tc_name = "tc_{0}{1}".format(tc_id, tc_postfix)
            if testgen(tc_name, conf):
                i += 1
                try:
                    dump_coverage(tc_name)
                except ValueError:#Exception:
                    print('problem in coverage')
                    LOG.error('COVERAGE EXCEPTION ' + tc_name)
            else:
                if i == newi:
                    retrycount += 1
                else:
                    newi = i
                    retrycount = 0

                if retrycount > 100:
                    worthy = False
                    
                # print 'Retrying', i
  if subject != 'js':
      run('rm -f tc_*.c '.format(directory))
  run('mv tc_* {0}'.format(directory))
  run('mv target*.cfg {0}'.format(directory))
  return i






generate_tests(GUIDEDTESTGEN_TIME, direct, glob.glob(os.path.join(direct, '*.cfg')))

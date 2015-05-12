import os
import myutils

curdir = os.getcwd()+ os.sep

JS = '../../spidermonkey/js1.6/src/Linux_All_DBG.OBJ/js -f '

GCOVDIR = curdir 
SRCDIR = '../../spidermonkey/js1.6/src/'
OBJDIR  = "../../spidermonkey/js1.6/src/Linux_All_DBG.OBJ/"

JSFUN_FUZ_PATH = "new_jsfunswarm2.js"
GITREPO = 'https://github.com/osustarg/spidermonkey.git'
gtg =  'https://github.com/alipourm/guided-random-testing.git'
bugs ={'bug1172': [18056, 18057, 18058, 18059, 18060, 18061, 18062, 18063, 19210, 19211, 19212, 19223, 19244, 19254, 19255], 'bug880': [19980, 19981, 19984, 19985, 20028], 'bug1294': [1368, 1369, 1370, 1371, 1372, 1373, 16170, 16171, 16172, 18938, 18939, 18940, 18941], 'bug297': [19121, 19122, 19123, 19124, 19125, 19126, 19127, 19128, 19129, 19130, 19131, 19132, 19133, 19134, 19135, 19136, 19137, 19138, 19139, 19140, 19141, 19142, 19143, 19144, 19145, 19146, 19147, 19148, 19149, 19150, 19151, 19152, 19153, 19154, 19155, 19156, 19157, 19158, 19159, 19160], 'bug297_2': [19962, 19963, 19964, 19965, 19966, 19967, 19968, 19969, 19970, 19971, 19972, 19973, 19974, 19975, 19976, 19977, 19978, 19979, 19980, 19981, 19982, 19983, 19984, 19985, 29194, 29201, 29221, 29222], 'bug95': [16997, 16998, 16999, 17000, 17001, 17002, 17003, 17004, 17005, 17006, 17007, 17008, 17009, 17010, 17011, 17008, 17009]}


def prepare(rootdir):
    cwd = os.getcwd()
    os.mkdir(rootdir)
    os.chdir(rootdir)
    print myutils.run('git clone {0}'.format(GITREPO))
    print myutils.run('git clone {0}'.format(gtg))
    os.chdir('spidermonkey/js1.6/src/')
    print myutils.run('make -f Makefile.ref')
    os.chdir(cwd)
    os.chdir(rootdir)
    os.chdir('guided-random-testing/src')
    print myutils.run('git fetch')
    print myutils.run('git checkout master')
    # myutils.run('python gtg.py js & > /dev/null')
    os.chdir(cwd)

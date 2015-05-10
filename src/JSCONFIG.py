import os
import myutils

curdir = os.getcwd()+ os.sep

JS = '../../spidermonkey/js1.6/src/Linux_All_DBG.OBJ/js -f '

GCOVDIR = curdir 
SRCDIR = '../../spidermonkey/js1.6/src/'
OBJDIR  = "../../spidermonkey/js1.6/src/Linux_All_DBG.OBJ/"

JSFUN_FUZ_PATH = "new_jsfunswarm2.js"
GITREPO = 'git@github.com:osustarg/spidermonkey.git'
gtg =  'git@github.com:alipourm/guided-random-testing.git'

def prepare(rootdir):
    cwd = os.getcwd()
    os.mkdir(rootdir)
    os.chdir(rootdir)
    print myutils.run('git clone {0}'.format(GITREPO))
    print myutils.run('git clone {0}'.format(gtg))
    os.chdir('spidermonkey/js1.6/src/')
    print myutils.run('gmake -f Makefile.ref -j 2')
    os.chdir(cwd)
    os.chdir(rootdir)
    os.chdir('guided-random-testing/src')
    print myutils.run('git fetch')
    print myutils.run('git checkout master')
    myutils.run('python gtg js & > /dev/null')
    os.chdir(cwd)

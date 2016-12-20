import os
import myutils

curdir = os.getcwd()+ os.sep
SRCDIR = os.path.join(myutils.BASE_DIRECTORY, 'yaffstest/yaffs2tester/')
OBJDIR  = os.path.join(myutils.BASE_DIRECTORY,'yaffstest/yaffs2tester/')
#GCOVDIR =  OBJDIR
GCOVDIR = curdir 

YAFSSTESTGEN_EXE = os.path.join(myutils.BASE_DIRECTORY,
    'yaffstest/yaffs2tester/testcasegenerator')
YAFFS = os.path.join(myutils.BASE_DIRECTORY, 'yaffstest/yaffs2tester/yaffs2_gcov ')


GITREPO = 'git@github.com:alipourm/yaffstest.git'
gtg =  'git@github.com:alipourm/guided-random-testing.git'

def prepare(rootdir):
    cwd = os.getcwd()
    os.mkdir(rootdir)
    os.chdir(rootdir)
    print myutils.run('git clone {0}'.format(GITREPO))
    print myutils.run('git clone {0}'.format(gtg))
    os.chdir('yaffstest/yaffs2tester/')
    print myutils.run('make -f TestMakefile')

    os.chdir(cwd)
    os.chdir(rootdir)
    os.chdir('guided-random-testing/src')
    print myutils.run('git fetch')
    print myutils.run('git checkout master')
    # print myutils.run('python gtg.py yaffs > /dev/null')
    os.chdir(cwd)

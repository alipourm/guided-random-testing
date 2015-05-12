import os
import myutils
curdir = os.getcwd()+ os.sep



SRCDIR = '../../gcc-4.4.7/host-x86_64-unknown-linux-gnu/gcc/'
OBJDIR  = '../../gcc-4.4.7/host-x86_64-unknown-linux-gnu/gcc/'
#GCOVDIR =  OBJDIR
GCOVDIR = curdir

CSMITHPATHINC = '~/tools/csmith/runtime'
CSMITH_EXE = '~/tools/csmithbin/bin/csmith'
GCC = '../../gcc/bin/gcc -O3 -I{0} '.format(CSMITHPATHINC)
GCCLOC='/nfs/stak/students/a/alipour/public_html/tmp/gcc-4.4.7.tar.gz'
gtg =  'git@github.com:alipourm/guided-random-testing.git'

def prepare(rootdir):
    cwd = os.getcwd()
    os.mkdir(rootdir)
    os.chdir(rootdir)
    print myutils.run('cp {0} .'.format(GCCLOC))
    myutils.run('tar -xvf gcc-4.4.7.tar.gz')
    myutils.run('rm -f gcc-4.4.7.tar.gz')
    os.chdir('gcc-4.4.7')
    gccdir = os.path.join(rootdir, 'gcc')
    print myutils.run('./configure --prefix={0} --enable-coverage --disable-bootstrap --enable-languages=c'.format(gccdir))
    print myutils.run('make -j 8')
    print myutils.run('make install')
    os.chdir(cwd)
    os.chdir(rootdir)
    print myutils.run('git clone {0}'.format(gtg))
    os.chdir('guided-random-testing/src')
    print myutils.run('git fetch')
    print myutils.run('git checkout master')
    os.chdir(cwd)

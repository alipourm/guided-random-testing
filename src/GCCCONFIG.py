import os
import myutils
curdir = os.getcwd()+ os.sep



SRCDIR = '../../gcc-4.4.7/host-x86_64-unknown-linux-gnu/gcc/'
OBJDIR  = '../../gcc-4.4.7/host-x86_64-unknown-linux-gnu/gcc/'
#GCOVDIR =  OBJDIR
GCOVDIR = curdir

CSMITHPATHINC = '/nfs/stak/students/a/alipourm/csmith/include/csmith-2.1.0'
CSMITH_EXE = '/nfs/stak/students/a/alipourm/csmith/bin'
GCC = '../../gcc/bin/gcc -w -O3 -I{0} -o /dev/null'.format(CSMITHPATHINC)
GCCLOC='/nfs/stak/students/a/alipourm/gcc-6.2.0.tar.gz'
gtg =  'https://github.com/alipourm/guided-random-testing.git'
def prepare(rootdir):
    cwd = os.getcwd()
    os.mkdir(rootdir)
    os.chdir(rootdir)
    print myutils.run('cp {0} .'.format(GCCLOC))
    myutils.run('tar -xvf *.tar.gz')
    myutils.run('rm -f *.gz')

    os.chdir('gcc-4.4.7')
    os.mkdir('build')
    os.chdir('build')
    gccdir = os.path.join(rootdir, 'gcc')
    myutils.run('../configure --prefix={0} --with-mpc=/scratch/alipourm/lib --enable-languages=c --disable-multilib '.format(gccdir))
    myutils.run('make -j 8')
    myutils.run('make install')
    os.chdir(cwd)
    os.chdir(rootdir)
    #print myutils.run('git clone {0}'.format(gtg))
    #os.chdir('guided-random-testing/src')
    #print myutils.run('git fetch')
    #print myutils.run('git checkout master')
    os.chdir(cwd)

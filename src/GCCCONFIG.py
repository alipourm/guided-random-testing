import os
import myutils
curdir = os.getcwd()+ os.sep



SRCDIR = None #'../../gcc-4.4.7/host-x86_64-unknown-linux-gnu/gcc/'
OBJDIR  = None #'../../gcc-4.4.7/host-x86_64-unknown-linux-gnu/gcc/'
#GCOVDIR =  OBJDIR
GCOVDIR = curdir

CSMITHPATHINC = '/nfs/stak/students/a/alipourm/csmith/include/csmith-2.2.0'
CSMITH_EXE = '/nfs/stak/students/a/alipourm/csmith/bin/csmith'
GCC = None
GCCLOC='/nfs/stak/students/a/alipourm/gcc-6.2.0.tar.gz'
gtg =  'https://github.com/alipourm/guided-random-testing.git'
def prepare(rootdir):
    global SRCDIR
    global OBJDIR
    global GCC
    SRCDIR = os.path.join(rootdir, 'gcc-6.2.0/host-x86_64-pc-linux-gnu/gcc/')
    OBJDIR = os.path.join(rootdir, 'gcc-6.2.0/host-x86_64-pc-linux-gnu/gcc/')
    GCC    = os.path.join(rootdir, 'gcc/bin/gcc -w -O3 -I{0} -o /dev/null'.format(CSMITHPATHINC))

    cwd = os.getcwd()
    try:
        os.mkdir(rootdir)
        gccdir = os.path.join(os.path.abspath(rootdir), 'gcc')
        os.chdir(rootdir)
        print myutils.run('cp {0} .'.format(GCCLOC))
        myutils.run('tar -xvf *.tar.gz')
        myutils.run('rm -f *.gz')
        os.chdir('gcc-6.2.0')
        print myutils.run('./configure --prefix={0} --with-mpc=/scratch/alipourm/lib --enable-languages=c --disable-bootstrap --enable-coverage --disable-multilib '.format(gccdir))
        print myutils.run('make -j 8')
        print myutils.run('make install')
        # exit(0)
    except Exception:
        pass
    #print myutils.run('git clone {0}'.format(gtg))
    #os.chdir('guided-random-testing/src')
    #print myutils.run('git fetch')
    #print myutils.run('git checkout master')
    os.chdir(cwd)

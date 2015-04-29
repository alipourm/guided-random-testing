import os

curdir = os.getcwd()+ os.sep



SRCDIR = '../../gcc-4.4.7/host-x86_64-unknown-linux-gnu/gcc/'
OBJDIR  = '../../gcc-4.4.7/host-x86_64-unknown-linux-gnu/gcc/'
#GCOVDIR =  OBJDIR
GCOVDIR = curdir 

CSMITHPATHINC = '/scratch/projects/csmith/runtime'
CSMITH_EXE = '/scratch/projects/csmithbin/bin/csmith'
GCC = '../../gcc/bin/gcc -O3 -I{0} '.format(CSMITHPATHINC)


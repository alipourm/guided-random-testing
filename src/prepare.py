import myutils
import sys
import os


subject = sys.argv[1]

if subject == 'yaffs':
    import YAFFSCONFIG as config
elif subject == 'js':
    import JSCONFIG as config
elif subject =='gcc':
    import GCCCONFIG as config

config.prepare(sys.argv[2])

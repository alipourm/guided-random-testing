from myutils import run
import GCCCONFIG

def testgen(tc_name, conf):
    print conf
    status, conf = run('python GCCswarmup.py {0} {1}'.format( conf, tc_name + '.conf'))
    print conf
    status, output = run('{0} {1} > {2}'.format(GCCCONFIG.CSMITH_EXE, conf, tc_name))
    print output
    return True

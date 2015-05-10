from myutils import run


def testgen(tc_name, conf):
    status, output = run('{0} {1} > {2}'.format(GCCCONFIG.CSMITH_EXE, conf, tc_name))
    return True

from myutils import run
import YAFFSCONFIG
import re


def testgen(tc_name, conf):
    status, yaffs_conf = run("python YAFFSswarmup.py {0}".format(conf))
    status, output = run('{0} --tclen 100 {1}'.format(YAFFSCONFIG.YAFSSTESTGEN_EXE, yaffs_conf))
    features = set(re.findall('\n(\d+),', output))
    features_str = ' '.join(features)
    open(tc_name, 'w').write(output)
    open(tc_name + '.conf', 'w').write(features_str)
    return True

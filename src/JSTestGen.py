from myutils import run
import re
import JSCONFIG




def testgen(tc_name, conf):
    status, output = run("python JSswarmup.py {0} {1} swarm.js {2}".format(JSCONFIG.JSFUN_FUZ_PATH, conf, tc_name + '.conf'))
    status, output = run("js -f swarm.js")
   

    filtered = filter(lambda s: s.startswith("try"), output.split('\n'))
    # print output
    # print 'TCLEN: {0}'.format(len(filtered))
    if len(filtered) == 100:
        outfn = open(tc_name, 'w')
        for l in filtered:
            outfn.write(l + '\n')
        outfn.flush()
        outfn.close()
        return True
    else:
        return False

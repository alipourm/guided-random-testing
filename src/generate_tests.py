import commands
import sys
import time


def run(cmd):
    return commands.getstatusoutput(cmd)

TIMELENGHT = 600 # 1 minute

i = 1
start = time.time()

conf = sys.argv[1]

while time.time()-start < TIMELENGHT:
    tc_id = str(i).zfill(7)
    status, output = run("python swarmup.py jsfunswarm.js  {0} swarm.js swarm.conf".format(conf))
    print status, output
    status, output = run("js -f swarm.js".format(dir))
    # print status, output
    # break
    filtered = filter(lambda s: s.startswith("try"), output.split('\n'))
    if len(filtered) == 1000:
        run("cp swarm.conf tc_{0}.conf".format(tc_id))
        outfn = open("tc_{0}.js".format(tc_id), 'w')
        for l in filtered:
            outfn.write(l + '\n')
        outfn.flush()
        outfn.close()
        i += 1 
    else:
        print 'Retrying', i
        

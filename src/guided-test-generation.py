import logging
import commands
import interaction
import pandas as pd
import os
import numpy as np
from coverage import Coverage
import pickle
# need for paralleization -- bottleneck is coverage


LOG = logging.getLogger('guided-test')
LOG.setLevel(logging.DEBUG)
fh = logging.FileHandler('execution.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
LOG.addHandler(fh)



def run(cmd):
    return commands.getstatusoutput(cmd)






def dump_coverage(f):
  c = Coverage(f)
  line_cov =  c.get_percent_line()
  print line_cov
  LOG.info('line_cov:' + str(line_cov)) 
  fn_cov = open(f + '.fcov', 'w')
  l_cov = open(f + '.lcov', 'w')
  br_cov = open(f + '.bcov', 'w')
  function_cov = c.functions
  branch_cov = c.get_b_cov()
  line_cov = c.get_l_cov()
  pickle.dump(function_cov, fn_cov)
  pickle.dump(branch_cov, br_cov)
  pickle.dump(line_cov, l_cov)
  

fst = lambda (x,y):x
snd = lambda (x,y):y
tonum = lambda s: int(re.findall("\d+", s)[0])



def generate_tests(time_length, directory, conf):
  i = 1
  start = time.time()
  while time.time()-start < time_length:
    tc_id = str(i).zfill(7)
    status, output = run("python swarmup.py jsfunswarm.js  {0} swarm.js swarm.conf".format(conf))
    # ls print status, output
    status, output = run("js -f swarm.js".format(dir))
    # print status, output
    # break
    filtered = filter(lambda s: s.startswith("try"), output.split('\n'))
    if len(filtered) == 1000:
      run("cp swarm.conf tc_{0}.conf".format(tc_id))
      tc_name = "tc_{0}.js".format(tc_id)
      outfn = open(tc_name, 'w')
      for l in filtered:
        outfn.write(l + '\n')
      outfn.flush()
      outfn.close()
      i += 1 
      dump_coverage(tc_name)
    else:
      print 'Retrying', i
  run('mv tc_* {0}'.format(directory))


def get_rels(l, r):
  return [i for i in l if i == r]


def count(l):
  I = get_rels(l,'I')
  S = get_rels(l,'S')
  T = get_rels(l,'T')
  return {'I':len(I),
          'S':len(S),
          'T':len(T)}


def agg_lines(df):
  lines = []
  for line in df:
    lines.append(line)
  return lines


def pick_target(df):
  relations =[k for k in df.columns if '_relation'in k]
  df['lineno']= df.index.copy()
  groups = df.groupby(relations)
  gr = groups['cov'].agg({'average':np.mean, 'count': np.size})
  gr['TEMP']=gr.index.copy()
  gr['I']= gr['TEMP'].apply(lambda row: count(row)['I'])
  gr['T']= gr['TEMP'].apply(lambda row: count(row)['T'])
  gr['S']= gr['TEMP'].apply(lambda row: count(row)['S'])
  gr = gr[(gr['T'] + gr['S'] > 0) & (gr['average'] < 200) & (gr['I']>250)]
  df2 = df.join(gr, how='right', on=gr.index.names)
  targets = df2[df2['T']<4][relations]
  return targets


def get_feature(f):
  # f\d+_relation
  return re.findall(r'\d+', f)[0]


def get_conf(targets):
  l = []
  for f in relations:
    feature_num = get_feature(f)
    if 'T' in targets[f]: 
      l.append('+' + feature_num)
    elif 'S' in targets[f]:
      l.append('+' + feature_num)
  return '\n'.join(l)



INIT_CONF = 'init.cfg'
TARGET_CONF = 'target.cfg'




import time
def main(experiment_no):
  cur_dir = os.curdir
  experiment_dir = os.path.join(cur_dir, str(experiment_no))
  os.mkdir(experiment_dir)
  # os.chdir(experiment_dir)
  directory = os.path.join(experiment_dir, 'init')
  LOG.info('Generating Initial Test Suite Started')
  generate_tests(3600, directory, INIT_CONF)
  LOG.info('Generating Initial Test Suite Ended')


  LOG.info('Calculating Targets Started')
  target_relation = interaction.get_feature_relations(directory + '/*.lcov')
  target_relation.to_csv('{0}/relations.csv', directory)
  LOG.info('Calculating Targets Ended')
 

  LOG.info('Pick Targets Started')
  targets = pick_target(target_relation)
  confs = get_conf(targets)
  conf_file = open(TARGET_CONF, 'w')
  conf_file.write(conf)
  conf_file.flush()
  conf_file.close()
  LOG.info('Pick Targets Ended')

  LOG.info('Generate MiniTests for Targets Started')
  for i in range(15):
    directory = os.path.join(experiment_dir, str(i))
    generte_tests(600, directory, TARGET_CONF)
  LOG.info('Generate MiniTests for Targets Ended')





main(1)

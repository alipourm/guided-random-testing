import logging
import commands
import interaction
import pandas as pd
import os
import numpy as np
from coverage import Coverage
import pickle
import consts
import re
import random
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
  print run('mv tc_* {0}'.format(directory))
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


LOWER_PRECENTAGE = 25
HIGHER_PERCENTAGE = 50
SAMPLE_SIZE = 30

def pick_target(df, relations, selection_fn):
  df['lineno']= df.index.copy()
  groups = df.groupby(relations)
  gr = groups['cov'].agg({'average':np.mean, 'median':np.median, 'count': np.size})
  gr['TEMP']=gr.index.copy()
  gr['I']= gr['TEMP'].apply(lambda row: count(row)['I'])
  gr['T']= gr['TEMP'].apply(lambda row: count(row)['T'])
  gr['S']= gr['TEMP'].apply(lambda row: count(row)['S'])
  [l,h] = np.percentile(gr['median'].values, [LOWER_PRECENTAGE, HIGHER_PERCENTAGE])
  gr = selection_fn(gr, l, h)
  print 'after call',  len(gr)
  try:  samples = gr.loc[random.sample(gr.index, SAMPLE_SIZE)]
  except ValueError: 
      LOG.debug('Sample larger than population')
      samples = gr
  return samples.index.get_values()






def get_feature(f):
  # f\d+_relation
  return re.findall(r'\d+', f)[0]



def get_conf(values, relations):
    l = []
    z = zip(values, relations)
    for x in z:
        feature_num = get_feature(x[1])
        if x[0] == 'T':
            l.append('+' + feature_num)
        elif x[0] == 'S':
            l.append('-' + feature_num)
    return '\n'.join(l)



INIT_CONF = 'init.cfg'
TARGET_CONF = 'target.cfg'
SEEDTESTGEN_TIME = 3600 
GUIDEDTESTGEN_TIME = 600

def select_all(gr, l, h):
    return gr

def select_2nd_quantile(gr, l, h): 
    return gr[(gr['median'] > l) & (gr['median'] < h)]  

def select_2nd_quantile_but_concise(gr, l, h): 
    return gr[(gr['median'] > l) & (gr['median'] < h) & (gr['I']>250) & (gr['T'] + gr['S'] > 0)]


selection_fn = [select_2nd_quantile, select_2nd_quantile_but_concise, select_all]

import time, glob
def main(experiment_no):
  LOG.info('experiment: ' + str(experiment_no))
  cur_dir = os.getcwd()
  experiment_dir = os.path.join(cur_dir, str(experiment_no))
  os.mkdir(experiment_dir)
  directory = os.path.join(experiment_dir, 'init')
  os.mkdir(directory)
  LOG.info('Generating Initial Test Suite Started')
  generate_tests(SEEDTESTGEN_TIME, directory, INIT_CONF)

  LOG.info('Generating Initial Test Suite Ended' + ' ' + directory)

  print directory
  LOG.info('Calculating Targets Started')
  target_relation = interaction.get_feature_relations(glob.glob(directory + '/*.lcov'))
  print target_relation
  target_relation.to_csv('{0}/relations.csv'.format(directory))
  LOG.info('Calculating Targets Ended')

  LOG.info('Pick Targets Started')
  relations =[k for k in target_relation.columns if '_relation'in k]
  print 'relations:', relations
  for fn in selection_fn:
      print fn.__name__
      targets = pick_target(target_relation, relations, fn)
      LOG.info('Pick Targets Ended')
      LOG.info('Generate MiniTests for Targets Started')
      i = 0
      os.mkdir(os.path.join(experiment_dir, fn.__name__))
      print len(targets)
      for t in targets:
          conf = get_conf(t, relations)
          LOG.info('Generate MiniTests for Targets Started' )
          LOG.info('Confg:' + conf)
          conf_file = open(TARGET_CONF, 'w')
          conf_file.write(conf)
          conf_file.flush()
          conf_file.close()
          directory = os.path.join(experiment_dir, fn.__name__,  str(i))
          os.mkdir(directory)
          generate_tests(GUIDEDTESTGEN_TIME, directory, TARGET_CONF)
          i = i + 1 
  LOG.info('Generate MiniTests for Targets Ended')



for i in range(20):
  print i
  main(i)

from coverage import Coverage
import GCCCONFIG

import commands
import consts
import interaction
import logging
import numpy as np
import os
import pandas as pd
import pickle
import random
import re
import sys
# need for paralleization -- bottleneck is coverage



LOG = logging.getLogger('GCC-guided-test')
LOG.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOG.name + '-debug.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
LOG.addHandler(fh)



def run(cmd):
#    print cmd
    return commands.getstatusoutput(cmd)


def dump_coverage(tcname):
  c = Coverage(tcname)
  line_cov = np.array(c.get_l_cov())
  print '{0} of {1}'.format(np.sum(line_cov), line_cov.size)
  LOG.info(tcname + '{0} of {1}'.format(np.sum(line_cov), line_cov.size))
  
  np.save(tcname, line_cov)




fst = lambda (x,y):x
snd = lambda (x,y):y
tonum = lambda s: int(re.findall("\d+", s)[0])

JSFUN_FUZ_PATH = "new_jsfunswarm2.js"


def generate_tests(time_length, directory, conf):
  i = 1
  start = time.time()
 
  while time.time()-start < time_length:
    tc_id = str(i).zfill(7)
    tc_name = "tc_{0}.c".format(tc_id)
    status, csmith_conf = run("python swarmup.py {0} {1}.conf".format(conf, tc_name))
    # ls print status, output

    print tc_name
    status, output = run('{0} {1} > {2}'.format(GCCCONFIG.CSMITH_EXE, csmith_conf, tc_name))

    # print status, output
    # break
    try:
        
        dump_coverage(tc_name)
    except ValueError:#Exception: 
        print('problem in coverage')
        LOG.error('COVERAGE EXCEPTION ' + tc_name)
    i += 1
  print run('mv tc_* {0}'.format(directory))
  print run('cp *.cfg {0}'.format(directory))



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


LOWER_PRECENTAGE = 10
HIGHER_PERCENTAGE = 30
SAMPLE_SIZE = 50

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
  # print 'after call',  len(gr)
  try:  
      samples = gr.loc[random.sample(gr.index, SAMPLE_SIZE)]
  except ValueError: 
      LOG.debug('Sample larger than population')
      samples = gr
  return samples



def pick_target_alex(df, relations):
  df['lineno']= df.index.copy()
  df2 = df[df['cov'] != 0]
  [l,h] = np.percentile(df2['cov'].values, [LOWER_PRECENTAGE, HIGHER_PERCENTAGE])
  gr = df2[(df2['cov'] >= l) & (df2['cov'] <= h)]
  try:  samples = gr.loc[random.sample(gr.index, SAMPLE_SIZE)]
  except ValueError: 
      LOG.debug('Sample larger than population')
      samples = gr
  # print 'samples:',  samples
  return samples


def pick_n_target(df, relations,n):
  df['lineno']= df.index.copy()
  df2 = df[df['cov'] != 0]
  [l,h] = np.percentile(df2['cov'].values, [LOWER_PRECENTAGE, HIGHER_PERCENTAGE])
  gr = df2[(df2['cov'] >= l) & (df2['cov'] <= h)]
  try:  samples = gr.loc[random.sample(gr.index, n)]
  except ValueError: 
      LOG.debug('Sample larger than population')
      samples = gr
  # print 'samples:',  samples
  return samples





def get_feature(f):
  # f\d+_relation
  return re.findall(r'\d+', f)[0]




feature_dict = {}
jsfunfuz = []

def load_jsfunrun():
    import re
    for l in open(JSFUN_FUZ_PATH):
        f = re.findall('##\d+##', l)
        if len(f) != 0 :
            feature_dict[l] = int(f[0][2:-2])
        jsfunfuz.append(l)






def pure_swarm(feature, suppressors, triggers):
    if random.randint(0,1) == 0:
        return True
    else:
        return False

def no_swarm(feature_num, suppressors,triggers):
    if feature_num in triggers:
        return True
    else:
        return False

def half_swarm(feature_num, suppressors, triggers):
    if feature_num in triggers:
        return True
    elif feature_num not in suppressors:
        return pure_swarm(feature_num, suppressors, triggers)
    else:
        return False



def create_test_generator(swarmification_fun, suppressors, triggers):
    fuzzer = []
    for l in jsfunfuz:
        if l in feature_dic:
            # so, it's a feature. Decide if you want to have it or no
            if swarmification_fun(feature_dict[l], suppressors,triggers):
                fuzzer.append(l)
        else:
            fuzzer.append(l)
    return fuzzer
    




def get_conf2(values, relations):
    suppressors = []
    triggers = []
    z = zip(values, relations)
    for x in z:
        feature_num = get_feature(x[1])
        if x[0] == 'T':
            triggers.append(feature_num)
        elif x[0] == 'S':
            suppressors.append(feature_num)
    return {'S':suppressors,
            'T':triggers}  


def get_conf(values, relations, sw_fn):
    l = []
    z = zip(values, relations)
    for x in z:
        feature_num = get_feature(x[1])
        if x[0] == 'T':
            l.append('++' + feature_num)
        elif x[0] == 'I':
            if sw_fn == half_swarm:
                l.append('+' +  feature_num)
    return '\n'.join(l)

def get_conf_alex(values, relations, sw_fn):
    l = []
    z = zip(values, relations)
    for x in z:
        feature_num = get_feature(x[1])
        if x[0] == 'T':
            l.append('++' + feature_num)
        elif x[0] == 'I':
            if sw_fn == half_swarm:
                l.append('+' +  feature_num)
    return '\n'.join(l)


INIT_CONF = 'init.cfg'
TARGET_CONF = 'target.cfg'
SEEDTESTGEN_TIME = 3600
GUIDEDTESTGEN_TIME = 600

def select_all(gr, l, h):
    return gr

def select_2nd_quantile(gr, l, h): 
    return gr[(gr['median'] >= l)]  

def select_2nd_quantile_but_concise(gr, l, h): 
    return gr[(gr['median'] > l) & (gr['median'] < h) & (gr['I']>250) & (gr['T'] + gr['S'] > 0)]


selection_fn = [select_2nd_quantile, select_2nd_quantile_but_concise, select_all]
swarmification_fn = [no_swarm, half_swarm]

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
  # print directory
  LOG.info('Calculating Targets Started')

  target_relation = interaction.get_feature_relations(glob.glob(directory + '/*.npy'))
  interaction.cleanup_summarize(directory , '/*.npy')


  # print target_relation
  target_relation.to_csv('{0}/relations.csv'.format(directory))
  LOG.info('Calculating Targets Ended')
  LOG.info('Pick Targets Started')
  relations =[k for k in target_relation.columns if '_relation'in k]
  # print 'relations:', relations

  targets = pick_target_alex(target_relation, relations)
  LOG.info('Generate MiniTests for Targets Started')

  for i in range(0, len(targets)):
      os.mkdir(os.path.join(experiment_dir, str(i)))
      print 'len(targets):', len(targets)
      for fn in swarmification_fn:
          print fn.__name__  
          t = targets.iloc[i]
          index = t.index
          conf = get_conf_alex(t[relations].values, relations, fn)
          if conf == '':
              LOG.info('All irrelevant for ' + str(t['lineno']))
              continue
          conf_file = open(TARGET_CONF, 'w')
          conf_file.write(conf)
          conf_file.flush()
          conf_file.close()
          directory = os.path.join(experiment_dir, str(i), fn.__name__)
          LOG.info("Targeted Test Begins")
          LOG.info('Directory:{0} Target:{1} ConfLen:{2}'.format(directory, str(t['lineno']), len(conf.split())))
          LOG.info('Target: ' + str(t['lineno']))
          LOG.info('Confg:\n' + conf)
          os.mkdir(directory)
          generate_tests(GUIDEDTESTGEN_TIME, directory, TARGET_CONF)

          interaction.cleanup_summarize(directory , '/*.npy')

          
  LOG.info('Generate MiniTests for Targets Ended')




def roundrobin(time_length, directory, configurationfiles):
  i = 1
  start = time.time()
 
  while time.time()-start < time_length:
    for conf in configurationfiles:
        if not time.time()-start < time_length:
            tc_id = str(i).zfill(7)
            tc_name = "tc_{0}.c".format(tc_id)
            status, csmith_conf = run("python swarmup.py {0} {1}.conf".format(conf, tc_name))
# ls print status, output

            print tc_name
            status, output = run('{0} {1} > {2}'.format(GCCCONFIG.CSMITH_EXE, csmith_conf, tc_name))

    # print status, output
    # break
            try:
        
                dump_coverage(tc_name)
            except ValueError:#Exception: 
                print('problem in coverage')
                LOG.error('COVERAGE EXCEPTION ' + tc_name)
            i += 1
  print run('mv tc_* {0}'.format(directory))
  print run('cp *.cfg {0}'.format(directory))


def multiline(directory, n, times = 5):
  target_relation = pd.DataFrame.from_csv('{0}/relations.csv')
  relations =[k for k in target_relation.columns if '_relation'in k]
  for i in range(times):
      targets = pick_n_target(target_relation, relations, n)
      confs = targets[relations].values
      lines = target['lineno'].values
      print 'targets:{0}'.format(lines)
      configurations = []
      for it, c in enumerate(confs):
          conf = get_conf_alex(c, relations, no_swarm) # we noswarm
          if conf == '':
              continue
          cfgname = TARGET_CONF + str(it)
          configurations.append(cfgname)
          conf_file = open(cfgname, 'w')
          configurations[]
          conf_file.write(conf)
          conf_file.flush()
          conf_file.close()
          
      exp_dir = os.path.join(directory, 'roundrobin_{0}_{1}'.format(i,n)
      os.mkdir(exp_dir)
      LOG.info("Targeted Multi Test Begins")
      LOG.info('Directory:{0} Targets:{1} N:{2}'.format(exp_dir, str(lines), len(lines)))
      roundrobin(GUIDEDTESTGEN_TIME, exp_dir, configurations)
      interaction.cleanup_summarize(exp_dir , '/*.npy')

dirs = sys.argv[1:]
print dirs
for d in dirs:
   multiline(os.path.join(d, 'init'), 4)




'''

start = int(sys.argv[1])
for i in range(start , start + 5):
  print i
  main(i)
'''

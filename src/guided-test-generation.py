import logging
import commands
import interaction
import pandas as pd
import os
import numpy as np
# need for paralleization -- bottleneck is coverage





def run(cmd):
    return commands.getstatusoutput(cmd)



conf = sys.argv[1]


def dump_coverage(f)
  c = Coverage(f)
  pbar.update(i)
  i += 1
  if os.path.exists(f + '.lcov'):
    continue
  fn_cov = open(f + '.fcov', 'w')
  l_cov = open(f + '.lcov', 'w')
  br_cov = open(f + '.bcov', 'w')
  function_cov = c.functions
  branch_cov = c.get_b_cov()
  line_cov = c.get_l_cov()
  #if line_cov[22385] == 1:
  #  print 'success'
  pickle.dump(function_cov, fn_cov)
  pickle.dump(branch_cov, br_cov)
  pickle.dump(line_cov, l_cov)

fst = lambda (x,y):x
snd = lambda (x,y):y
tonum = lambda s: int(re.findall("\d+", s)[0])
relations =[k for k in df.columns if '_relation'in k]


def generate_tests(time_length, directory, conf):
  i = 1
  start = time.time()
  while time.time()-start < time_length:
    tc_id = str(i).zfill(7)
    status, output = run("python swarmup.py jsfunswarm.js  {0} swarm.js swarm.conf".format(conf))
    print status, output
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


def get_targets(df):
  df['lineno']= df.index.copy()
  groups = df.groupby(relations)
  gr = groups['cov'].agg({'average':np.mean, 'count': np.size})
  gr['TEMP']=gr.index.copy()
  gr['I']= gr['TEMP'].apply(lambda row: count(row)['I'])
  gr['T']= gr['TEMP'].apply(lambda row: count(row)['T'])
  gr['S']= gr['TEMP'].apply(lambda row: count(row)['S'])
  gr = gr[(gr['T'] + gr['S'] > 0) & (gr['average'] < 200) & (gr['I']>250)]
  df2 = df.join(gr, how='right', on=gr.index.names)
  targets = df2[df2['T']==1][relations]

  

  return targets

def get_feature(f):
  # f\d+_relation
  pass

def get_conf(targets):
  for f in relations:
    if 'T' in targets[f]: pass
    elif: pass
      




LOG = logging.getLogger('guided-test')
LOG.setLevel(LOG.DEBUG)

def main():
  # 1. generate tests for 3600 seconds (i.e. 30 minutes) # it must be with coverage
  LOG.info('Generating Initial Test Suite Started')
  generate_tests(3600, directory, initial_conf)
  LOG.info('Generating Initial Test Suite Ended')
  # 2. calculate coverage
  LOG.info('Calculating Coverage Started')
  calculate_coverage(directory)
  LOG.info('Calculating Coverage Ended')
  # 2.5 find trigger/supressor relations
  LOG.info('Calculating Targets Started')
  target_relation = interaction.get_feature_relations(directory + '/*.lcov')
  target_relation.to_csv('{0}/relations.csv', directory)
  LOG.info('Calculating Targets Ended')
  # 2.6 choose targets
  LOG.info('Pick Targets Started')
  conf = pick_target(target_relation)
  LOG.info('Pick Targets Ended')
  # 3. generate tests based on the information in step 1  for 600 seconds (i.e 10 minutes)(15 times)
  LOG.info('Generate MiniTests for Targets Started')
  generte_tests(600, directory, conf)
  LOG.info('Generate MiniTests for Targets Ended')

  # 4. calculate coverage
  LOG.info('Calculating MiniTests for Targets Started')
  calculate_coverage
  LOG.info('Calculating MiniTests for Targets Ended')
  # 5. calculate the new medians

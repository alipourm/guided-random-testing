import commands
import logging
import os
import pickle
import random
import re
import time
import glob
import logging
import sys
import numpy as np
import pandas as pd
import aggressive
# NOTEneed for paralleization -- bottleneck is coverage


subject = sys.argv[1]
print subject
if subject == 'gcc':
    import GCCconsts as consts
    from GCCCoverage import Coverage
    from GCCTestGen import testgen
    LOG = logging.getLogger('GCC')
    INIT_CONF = 'GCCinit.cfg'
    SEEDTESTGEN_TIME = 3600
    GUIDEDTESTGEN_TIME = 600
    tc_postfix = '.c'

elif subject == 'yaffs':
    import YAFFSConsts as consts
    from YAFFSCoverage import Coverage
    from YAFFSTestGen import testgen
    LOG = logging.getLogger('YAFFS')
    INIT_CONF = 'YAFFSinit.cfg'
    SEEDTESTGEN_TIME = 900
    GUIDEDTESTGEN_TIME = 300
    tc_postfix = '.c'
elif subject == 'js':
    import JSCONSTS as consts
    from JSCoverage import Coverage
    from JSTestGen import testgen
    import JSCONFIG as config
    LOG = logging.getLogger('JS')
    INIT_CONF = 'JSinit.cfg'
    SEEDTESTGEN_TIME = 1800
    GUIDEDTESTGEN_TIME = 600
    tc_postfix = '.js'

os.mkdir(sys.argv[2])




LOG.setLevel(logging.DEBUG)
fh = logging.FileHandler('{0}/{1}-debug.log'.format(sys.argv[2], LOG.name), mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
LOG.addHandler(fh)


def run(cmd):
    # print cmd
    return commands.getstatusoutput(cmd)



def F((l, h), r):
    if np.isnan(l):
      l = 0
      h = 1
    if l <= r <= h:
        return consts.IRRELAVENT
    if l > r:
        return consts.TRIGGER
    if h < r:
        return consts.SUPRESSOR

Z = 1.96

def wilson_score_interval (n, n_f, r):
    z = Z
    p = (1.*n_f)/ n
    term1 = p + (z * z) / (2.*n)
    plus_minus = z * np.sqrt ((p * (1. - p) / n) + (z * z / (4. * n * n)))
    term2 = 1. + (z * z / n)
    low = (term1 - plus_minus) / term2
    high = (term1 + plus_minus) / term2
    k =  zip(low, high)
    k2 = pd.Series(k)
    s = k2.apply(lambda x: F(x, r))
    return s


def conf_file(test):
    return  open('{0}.conf'.format(test)).read().strip().split()


'''
def compute_wilson(covering_tests, location):
    n = 0
    feature_occurance = {}
    for f in range(consts.FEATURES_MIN, consts.FEATURES_MAX + 1):
        feature_occurance[f] = 0
    for test in covering_tests:
       for f in conf_file(test):
          feature_occurance[f] += 1
    wilson = {}
    for f in feature_occurance:
       wilson[f] = wilson_score_interval(len(covering_tests), float(feature_occurance[f])/len(covering_tests))
    return wilson
'''

def get_total_coverage(coverage_files):
  """
  pre: len(coverage_files) > 0
  """
  if len(coverage_files) == 0:
    return np.array([])
  first = coverage_files[0]
  rest = coverage_files[1:]
  coverage_vector = pickle.load(open(first))
  for f in rest:
    try:
        coverage_vector = np.add(coverage_vector, pickle.load(open(f)))
    except EOFError, ValueError:
        LOG.info('Error in adding {0}'.format(0))
        pass
  return  coverage_vector


def load_data(coverage_files):
  df = pd.DataFrame(get_total_coverage(coverage_files))
  df.columns = ['cov']
  return df




def add_features(df, coverage_files):
  feature_occurance = {}
  feature_freq = {}
  for f in range(consts.FEATURES_MIN, consts.FEATURES_MAX + 1):
    df['f' + str(f)] = 0
    feature_freq[f] = 0
  for cf in coverage_files:
    # print cf
    tc = '.'.join(cf.split('.')[:-1])
    try:
      coverage = np.array(pickle.load(open(cf)))
      for f in conf_file(tc):
          if consts.FEATURES_MIN <= int(f) <= consts.FEATURES_MAX:
              df['f' + str(f)] += coverage
              feature_freq[int(f)] += 1
    except EOFError:
       print cf
  return {'df': df,
          'feature_freq': feature_freq}






def cleanup_summarize(directory, filepattern):
  coverage_files = glob.glob(directory + filepattern)
  coverage = get_total_coverage(coverage_files)
  np.save(os.path.join(directory, consts.COVSUMMARYFILE), coverage)
  covpattern = os.path.join(directory, "tc_*.lcov")
  confpattern = os.path.join(directory, "tc_*.conf")
  tcpatterns = os.path.join(directory, "tc_*.c") # we need to keep .js files
  # run('rm -f {0} {1} {2}'.format(covpattern, confpattern, tcpatterns))



def get_feature_relations(coverage_files):
    df = load_data(coverage_files)
    # print 'loading data done'
    data = add_features(df, coverage_files)
    # print 'adding features  done'
    feature_freq = data['feature_freq']
    # print 'frequecied done data done'
    df = data['df']
      # df = df1[df1['cov'] > 0]
    for f in range(consts.FEATURES_MIN, consts.FEATURES_MAX + 1):
        # print f
        r = float(feature_freq[f])/ len(coverage_files)
        df['f' + str(f) + '_relation'] = wilson_score_interval(df['cov'], df['f' + str(f)], r)
        print 'after {0}'.format(f)
    return df











first_time_coverage_calc = False
def dump_coverage(f):
    global first_time_coverage_calc
    c = Coverage(f)
    if (not first_time_coverage_calc) and subject == 'gcc':
        fname = 'coverage_map.p'
        LOG.info("Dumping coverage map at: {0}".format(fname))
        maps = c.get_mapping()
        pickle.dump(maps, open(fname, 'wb'))
        first_time_coverage_calc = True
        exit(0)
    if subject == 'js':
        if 'ALL OK' not in c.output or 'ASSERT' in c.output:
            LOG.info('ASSERT in:{0}'.format(f))
            fout = open(f + '.out', 'w')
            fout.write(c.output)
            fout.close()
    # pline_cov = c.get_percent_line()
    # print line_cov
    l_cov = open(f + '.lcov', 'w')
    line_cov = c.get_l_cov()
    # LOG.info('line_cov: {0} | {1} out of {2}'.format(pline_cov, np.sum(line_cov), len(line_cov)))
    pickle.dump(line_cov, l_cov)

  

fst = lambda (x,y):x
snd = lambda (x,y):y
tonum = lambda s: int(re.findall("\d+", s)[0])


def generate_tests(time_length, directory, confs):
  i = 0
  start = time.time()
  # print conf
  retrycount = 0
  newi = 0
  worthy = True

  # print 'confs:', confs
  while time.time()-start < time_length and worthy and len(confs) > 0:
        for conf in confs:
          if time.time()-start < time_length:
            tc_id = str(i).zfill(7)
            tc_name = "tc_{0}{1}".format(tc_id, tc_postfix)
            if testgen(tc_name, conf):
                i += 1
                try:
                    dump_coverage(tc_name)
                except ValueError:#Exception:
                    print('problem in coverage')
                    LOG.error('COVERAGE EXCEPTION ' + tc_name)
            else:
                if i == newi:
                    retrycount += 1
                else:
                    newi = i
                    retrycount = 0

                if retrycount > 100:
                    worthy = False
                    
                # print 'Retrying', i
  if subject != 'js':
      run('rm -f tc_*.c '.format(directory))
  run('mv tc_* {0}'.format(directory))
  run('mv target*.cfg {0}'.format(directory))
  return i


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


LOWER_COVERAGE_RATE = 0.1
HIGHER_COVERAGERATE = 0.3
SAMPLE_SIZE = 20
'''
def pick_target(df, relations, selection_fn):
  df['lineno']= df.index.copy()
  groups = df.groupby(relations)
  gr = groups['cov'].agg({'average':np.mean, 'median':np.median, 'count': np.size})
  gr['TEMP']=gr.index.copy()
  gr['I']= gr['TEMP'].apply(lambda row: count(row)['I'])
  gr['T']= gr['TEMP'].apply(lambda row: count(row)['T'])
  gr['S']= gr['TEMP'].apply(lambda row: count(row)['S'])
  [l,h] = np.percentile(gr['median'].values, [LOWER_COVERAGE_RATE*100, HIGHER_COVERAGERATE*100])
  gr = selection_fn(gr, l, h)
  try:
      samples = gr.loc[random.sample(gr.index, SAMPLE_SIZE)]
  except ValueError: 
      LOG.debug('Sample larger than population')
      samples = gr
  return samples


def select_all(gr, l, h):
    return gr

def select_2nd_quantile(gr, l, h):
    return gr[(gr['median'] >= l)]

def select_2nd_quantile_but_concise(gr, l, h):
    return gr[(gr['median'] > l) & (gr['median'] < h) & (gr['I']>250) & (gr['T'] + gr['S'] > 0)]


'''


def pick_target(df, testsuitesize, lo, hi, samplesize):
    # testsuitesize = len(glob.glob(os.path.join(directory, 'tc_*')))/2
    [l, h] = [lo*testsuitesize, hi*testsuitesize]
    gr = df[(df['cov'] >= l) & (df['cov'] <= h)]
    try:
      samples = gr.loc[random.sample(gr.index, samplesize)]
    except ValueError:
      [l, h] = [l/2., h*1.5]
      try:
          gr = df[(df['cov'] >= l) & (df['cov'] <= h)]
          samples = gr.loc[random.sample(gr.index, samplesize)]
      except ValueError:
          samples = gr
    return samples


def regression(df, lines):
    df['lineno'] = df.index.copy()
    return df.loc[lines]



def get_feature(f):
  # f\d+_relation
  return re.findall(r'\d+', f)[0]



modes = ['halfswarm', 'noswarm', 'nosup']


def get_conf(values, relations, mode):
    l = []
    z = zip(values, relations)
    for x in z:
        feature_str = get_feature(x[1])
        if mode == 'fullrandom':
            l.append('++' + feature_str)
        elif mode == 'nosup':
            if x[0] != 'S':
                l.append('++' + feature_str)
        else:
            if x[0] == 'T':
                l.append('++' + feature_str)
            elif x[0] == 'I':
                if mode == 'halfswarm':
                    l.append('+' + feature_str)
    # print mode, l
    # print 'suppressors', sum([1 for s in values if s=='S'])
    return '\n'.join(l)


def init(experiment_dir):

    directory = os.path.join(experiment_dir, 'init')
    os.mkdir(directory)
    LOG.info('Generating Initial Test Suite Started')
    testsuitesize = generate_tests(SEEDTESTGEN_TIME, directory, [INIT_CONF])
    LOG.info('Directory:{0} TSSIZE:{1}'.format(directory, testsuitesize))
    LOG.info('Calculating Targets Started')
    target_relation = get_feature_relations(glob.glob(directory + '/*.lcov'))
    LOG.info('Calculating Targets Ended')

    cleanup_summarize(directory , '/*.lcov')
    # print 'cleanup done'
    # print target_relation
    target_relation.to_csv('{0}/relations.csv'.format(directory))
    # print 'tocsv done'
    return {'df': target_relation,
            'tssize': testsuitesize}


def individual(configurations, targets):
    results = []
    if len(configurations) != len(targets):
        print 'Inequal target and confs'
        exit(1)
    for j in range(len(configurations)):
        results.append((configurations[j], targets[j]))
    return results


def roundrobin_merge(configurations, targets):
    if len(configurations) != len(targets):
        print 'Inequal target and confs'
        exit(1)
    k =  zip(configurations, targets)
    # print 'round robin end:', k
    return [(c, [t]) for (c,t) in k]


def amRestrict(me, other):
    newme, newother = map(list, [me[0], other[0]])
    for i in range(len(newme)):
        # print  me[i]
        if newme[i] != newother[i] and newother[i] != 'I':
            return False
    return True



def merge_agrressive(configurations, targets):
    m = aggressive.Aggressive(configurations)
    res = m.minimize()
    return [(c, 0) for c in res]

def merge_greedy(configurations, targets):
    if len(configurations) != len(targets):
        print 'Inequal target and confs'
        exit(1)
    cp = [(c, [target]) for (c, target) in zip(configurations, targets)]
    # print 'cp', cp
    
    eliminated = []
    for i, c1 in enumerate(cp):
        for c2 in cp[i+1:]:
            if amRestrict(c1, c2):
                eliminated.append(c2[1])
                for k in c2[1]:
                    c1[1].append(k)
    
    # print 'after', cp
    # print 'elem', eliminated
    results = []
    for (c, lines) in cp:
        # print 'conf', c
        if lines not in eliminated:
            # print type(c), c.shape
            # for i in lines:
                results.append((c,lines))
    return results


def targetedtest(targetsdf, experiment_dir, merge_function):
    os.mkdir(experiment_dir)
    relations =[k for k in targetsdf.columns if '_relation'in k]
    configurations = targetsdf[relations].values
    targets = targetsdf.index
    newconfigurations = merge_function(configurations, targets)
    # print 'newconf', newconfigurations
    for mode in modes:
        conffiles = []
        for k, clist in enumerate(newconfigurations):
                # print 'k:', k
                #'clist:', clist
                (c, t) = clist
                conf = get_conf(c, relations, mode)
                # print '- m:{0} c:{1}'.format(merge_function.__name__, conf)
                if conf == '':
                    continue
                cfn = 'target{0}.cfg'.format(k)
                conffiles.append(cfn)
                conf_file = open(cfn, 'w')
                conf_file.write(conf)
                conf_file.flush()
                conf_file.close()
        LOG.info("Targeted Test Begins")
        directory = os.path.join(experiment_dir, mode)
        os.mkdir(directory)
        LOG.info('Confg:{0}'.format(conffiles))
        tssize = 0
        if 'regression' in experiment_dir:
            tssize = generate_tests(GUIDEDTESTGEN_TIME*3, directory, conffiles)
        else:
            tssize = generate_tests(GUIDEDTESTGEN_TIME, directory, conffiles)
        LOG.info('Directory:{0} Target:{1}, Mode:{2}, Merge:{3}, BeforeMerge:{4}, AfterMerge:{5}, TSSIZE:{6}'.format(directory, list(targets), mode, merge_function.__name__, len(targets), len(newconfigurations), tssize))
        cleanup_summarize(directory, '/*.lcov')
    LOG.info('Generate MiniTests for Targets Ended')




def getfullrandom():
    l = []
    for i in range(consts.FEATURES_MIN, consts.FEATURES_MAX+1):
        l.append('++{0}'.format(i))
    return '\n'.join(l)

FULLRANDOMCFG='fullrandom.cfg'

def dofullrandom(directory):
    conf = getfullrandom()
    conf_file = open(FULLRANDOMCFG, 'w')
    conf_file.write(conf)
    conf_file.flush()
    conf_file.close()
    newdir = os.path.join(directory, 'random')
    os.mkdir(newdir)
    LOG.info("RANDOM Test Begins")
    LOG.info('Directory:{0} Mode:{1}'.format(newdir, 'fullrandom'))
    generate_tests(GUIDEDTESTGEN_TIME, newdir, [FULLRANDOMCFG])
    LOG.info("RANDOM Test Ends")
          


def experiment(i):
    res = init(i)
    df = res['df']
    tssize = res['tssize']
    # print 'back from df'
    relations =[k for k in df.columns if '_relation'in k]
    # print relations
    # print 'before groupby df'
    gr = df.groupby(relations)
    # print 'after groupby df'
    # print 'gr', gr
    
    LOG.info('Groups:{0}'.format(len(gr.groups)))
    for p, g in gr:
        LOG.info('GLEN:{0} G:{1}'.format(len(g), p))

    # print 'before groupby df'
            
    # regressionsizes = [1,2,3,4,5,10,20]
    regressionsizes = [5,10,20]
    random.shuffle(regressionsizes)


    for k in range(5):
        for r in regressionsizes:
            target = pick_target(df,tssize, 0.1, 0.3, r)
            if r != 1:
                targetedtest(target,'{0}/greedy.{1}.{2}'.format(i, k, r), merge_greedy)
                targetedtest(target,'{0}/aggressive.{1}.{2}'.format(i, k, r), merge_agrressive)
            targetedtest(target,'{0}/roundroubin.{1}.{2}'.format(i, k, r), roundrobin_merge)

    if subject == 'js':
        bugs = config.bugs.keys()
        random.shuffle(bugs)
        for b in bugs:
         # print 'targetting', b, config.bugs[b]
            target = regression(df, config.bugs[b])
            targetedtest(target,'{0}/regression.greedy.{1}'.format(i, b), merge_greedy)
            targetedtest(target,'{0}/regression.roundrobin.{1}'.format(i, b), roundrobin_merge)
            targetedtest(target,'{0}/regression.aggresive.{1}'.format(i, b), merge_agrressive)



    dofullrandom(i)    



if __name__ == '__main__':
    experiment(sys.argv[2])


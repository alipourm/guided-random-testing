from math import sqrt
import Configuration
import consts
import glob
import numpy as np
import os
import pandas as pd
import pickle
import testgen


def F((l , h), r):
  if np.isnan(l):
    l = 0
    h = 1
  if l <= r and r <= h:
    return consts.IRRELAVENT
  if l > r:
    return consts.TRIGGER
  if h < r:
    return consts.SUPRESSOR



def wilson_score_interval (n, n_f, r):
  z = consts.Z
  p = (1.*n_f)/ n
  term1 = p + (z * z) / (2.*n)
  plus_minus = z * np.sqrt ((p * (1. - p) / n) + (z * z / (4. * n * n)))
  term2 = 1. + (z * z  / n)
  low = (term1 - plus_minus) / term2
  high = (term1 + plus_minus) / term2
  k =  zip(low, high)
  k2 = pd.Series(k)
  s  = k2.apply(lambda x: F(x, r))
  return s



def guided_random_testing(test_object, configuration):
  print 'Testing', test_object.name
  conf  = configuration.initialize()
  epoch = 0
  while not configuraion.stop_condition():
    epoch += 1
    configuraion.report(conf, epoch, consts.CONFIGURATION)
    feedback = test_object.test(conf)
    configuraion.report(feedback, epoch, consts.FEEDBACK)
    conf = Configuraiton.analyze_feedback(feedback)
    print 'epoch {0}'.format(epoch)




def conf_file(test):
  import re
  str_tcfile = open(get_test_name(test) + '.js').read()
  k = set(re.findall("##\d+##", str_tcfile))
  return map(lambda s: int(s[2:-2]), k)



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



def get_test_name(filename):
  """
  Assumes that the directories does not have '.' in their names.
  """
  return filename.split('.')[0] 



def get_covering_tests(location, coverage_files):
  covering_tests = []
  for cf in coverage_files:
    coverage_vector = pickle.load(open(cf))
    if coverage_vector[location] != 0:
      covering_tests.append(get_test_name(cf))
  
  return covering_tests







def low_outliers(data, m=1.):
  """
  Adopted from: 
  http://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
  """
  t = data['cov'].unique()
  print t['cov'].mean()- m * np.std(t['cov'])
  return {'locations':np.argwhere(np.mean(data2) - data > m * np.std(data2)),
           'values': data[np.mean(data2) - data > m * np.std(data2)]}




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
    print f
    try:
      coverage_vector = np.add(coverage_vector, pickle.load(open(f)))
    except EOFError:
      pass
  return  coverage_vector
  

def load_data(coverage_files):
  df = pd.DataFrame(get_total_coverage(coverage_files))
  df.columns = ['cov']
  return df

def plot_coverage(cov_vector):
  hist, bins = np.histogram(x, bins=50)
  width = 0.7 * (bins[1] - bins[0])
  center = (bins[:-1] + bins[1:]) / 2
  plt.bar(center, hist, align='center', width=width)
  plt.show()



def experiment_spidermonkey(observation_files):
  for f in observation_files:
    lines = open(f).readlines()
    lines = map(lambda s: s.stip(), lines)
    lines = filter(lambda s: s != '', lines)
    
    
  
def add_features(df, coverage_files):
  feature_occurance = {}
  feature_freq = {}
  for f in range(consts.FEATURES_MIN, consts.FEATURES_MAX + 1):
    df['f' + str(f)] = 0
    feature_freq[f] = 0
  for cf in coverage_files:
    print cf
    try:
      coverage = np.array(pickle.load(open(cf)))
      for f in conf_file(cf):
        df['f' + str(f)] += coverage
        feature_freq[f] += 1
    except EOFError:
      print cf
  return {'df': df,
          'feature_freq': feature_freq}
    


def cleanup_summarize(directory, filepattern):
  coverage_files = glob.glob(directory + filepattern)
  coverage = get_total_coverage(coverage_files)
  np.save(os.path.join(directory, consts.COVSUMMARYFILE), coverage)
  for cf in coverage_files:
    os.remove(cf)



def get_feature_relations(coverage_files):
  df = load_data(coverage_files)
  data = add_features(df, coverage_files)
  feature_freq = data['feature_freq']
  df = data['df']
  # df = df1[df1['cov'] > 0]
  for f in range(consts.FEATURES_MIN, consts.FEATURES_MAX + 1):
    print f 
    r = float(feature_freq[f])/ len(coverage_files)
    df['f' + str(f) + '_relation'] = wilson_score_interval(df['cov'], df['f' + str(f)], r)

  
  return df

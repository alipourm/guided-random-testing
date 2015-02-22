import Configuration
#import TestObject
import testgen
import consts
from math import sqrt
import numpy as np
import pickle
import glob
import pandas as pd






def wilson_score_interval (n, p):
  z = consts.Z
  term1 = p + (z * z) / (2.*n)
  plus_minus = z * sqrt ((p * (1. - p) / n) + (z * z / (4. * n * n)))
  term2 = 1. + (z * z  / n)
  return {'low': (term1 - plus_minus) / term2, 
          'high':(term1 + plus_minus) / term2 }




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
  str_features = open(test + '.conf').read().split()
  return map(lambda s: int(s.replace('--', '')), str_features)



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
  for 
  print t['cov'].mean()- m * np.std(t['cov'])
  return 
{ 'locations':np.argwhere(np.mean(data2) - data > m * np.std(data2)),
           'values': data[np.mean(data2) - data > m * np.std(data2)]}




def get_total_coverage(coverage_files):
  """
  pre: len(coverage_files) > 0
  """
  first = coverage_files[0]
  rest = coverage_files[1:]
  coverage_vector = pickle.load(open(first))
  for f in rest:
    # print f
    coverage_vector = np.add(coverage_vector, pickle.load(open(f)))

  return  coverage_vector
  

def load_data(coverage_files):
  df = pd.DataFrame()
  first = coverage_files[0]
  rest = coverage_files[1:]
  coverage_vector = pickle.load(open(first))
  for f in rest:
    coverage_vector = np.add(coverage_vector, pickle.load(open(f)))


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
    
    
  



def main():
  df = pd.DataFrame()
  coverage_files = glob.glob("/scratch/projects/guided_fuzzing/testcases/suite_1/*11.js.lcov")
  print coverage_files
  print 'Computing deprived ...'
  coverage_vector = get_total_coverage(coverage_files)
  deprived = low_outliers(coverage_vector)
  print 'deprived:', deprived
  targets = deprived['locations']

  print len(targets)
  
  exit(0)
  for t in targets:
    if coverage_vector[t] != 0:
      covering_tests = get_covering_tests(t, coverage_files)
      print compute_wilson(covering_tests, t)
  

main()




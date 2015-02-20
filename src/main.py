import Configuration
#import TestObject
import testgen
import consts
from math import sqrt
import numpy as np
import pickle
import glob
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






def low_outliers(data, m=2):
  """
  Adopted from: 
  http://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
  """
  return { 'locations':np.argwhere(np.mean(data) - data > m * np.std(data)),
           'values': data[np.mean(data) - data > m * np.std(data)]}




def find_rarely_covered(coverage_files):
  """
  pre: len(coverage_files) > 0
  """
  first = coverage_files[0]
  rest = coverage_files[1:]
  coverage_vector = pickle.load(open(first))
  for f in rest:
    print f
    coverage_vector = np.add(coverage_vector, pickle.load(open(f)))
  #  print coverage_vector
  #print 'computing outlier'
  #target = low_outliers(coverage_vector)
  # print zip(target['locations'], target['values'])
  return coverage_vector
  


# find_rarely_covered(glob.glob("/scratch/projects/guided_fuzzing/testcases/suite_1/*.lcov"))

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
  pass




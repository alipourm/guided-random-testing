import Configuration
import TestObject
import testgen
import consts




def wilson_score_interval (n, p):
  z = 
  term1 = p + (z * z) / (2*n)
  double plus_minus = z * math.sqrt ((p * (1 - p) / n) + (z * z / (4 * n * n)))
  double term2 = 1 + (z * z  / n)
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


def main():
  pass




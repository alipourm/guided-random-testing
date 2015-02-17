from abc import ABCMeta, abstractmethod
import sys
import consts

class Configuration:
  __metaclass__ = ABCMeta

  def __init__(self):
    self.outstream = sys.stdout


  @abstractmethod
  def initialize(self):
    """
    initializes the configuraiotns, which includes: loading list of faetures, ...
    """
    raise NotImplemented

  @abstractmethod
  def analyze_feedback(self, feedback):
    raise NotImplemented

  def report(self,  data, epoch, mode):
    if mode == consts.FEEDBACK:
      self.log('FEEDBACk: {0}, {1}\n'.format(epoch, str(data)))
    elif mode == const.CONFIGURATION:
      self.log('CONFIGURATION: {0}, {1}\n'.format(epoch, str(data)))
    else:
      raise NotImplemented

  def log(self, text):
    outstream.write(text)
    outstream.flush()
    

  
    
    

from abc import ABCMeta, abstractmethod
import Configuration

class TestObject:
  __metaclass__ = ABCMeta
  self.name = ''

  @abstractmethod
  def test(configuraion):
    """
    returns feedback
    """
    raise NotImplemented

  
  

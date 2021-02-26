from abc import ABC, abstractmethod

class ITest(ABC):
  @abstractmethod
  def generateData(self):
    pass
  @abstractmethod
  def test(self, **kwargs):
    pass
from abc import ABC, abstractmethod
from math import log
from utils import factorial

class IFunction(ABC):
  def __eq__(self, other):
    return str(self) == str(other)
  @abstractmethod
  def optimize(self):
    pass
  @abstractmethod
  def derivative(self):
    pass
  @abstractmethod
  def getVariables(self):
    pass
  @abstractmethod
  def operation(self, coordinate):
    pass

class Variable(IFunction):
  def __init__(self, name):
    self.name = name
  def __str__(self):
    return self.name
  def optimize(self):
    return self
  def derivative(self):
    return Constant(1)
  def getVariables(self):
    return [self]
  def operation(self, coordinate):
    return coordinate[self.name]

class Constant(IFunction):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)
  def optimize(self):
    return self
  def derivative(self):
    return Constant(0)
  def getVariables(self):
    return []
  def operation(self, coordinate):
    return self.value

class BinaryFunction(IFunction):
  def __init__(self, x1, x2, keyWord=''):
    self.x1=x1
    self.x2=x2
    self.keyWord = keyWord

  def __str__(self):
    return self.keyWord+'('+str(self.x1)+', '+str(self.x2)+')'

  def getVariables(self):
    vars1 = self.x1.getVariables()
    if not self.x2: return vars1
    return vars1 + [v for v in self.x2.getVariables() if v not in vars1]

  def derivative(self):
    if len(self.getVariables()) > 1:
      print("Only functions with at most one variable can be derived at this time")
      return
    return self._derivative()
  
  def _derivative(self):
    pass

  def operation(self,coords):
    if self.x2 == None:
      return self._operation(self.x1.operation(coords), None)
    return self._operation(self.x1.operation(coords), self.x2.operation(coords))

  def _operation(self, x1, x2):
    pass

  def optimize(self):
    pass

class Identity(BinaryFunction):
  def __init__(self, x1):
    super(Identity, self).__init__(x1, None, keyWord='Id')
  def _operation(self, x, y):
    return x
  def _derivative(self):
    return Identity(self.x1.derivative())
  def optimize(self):
    return self.x1.optimize()
  
class Addition(BinaryFunction):
  def __init__(self, x1, x2):
    super(Addition, self).__init__(x1, x2, keyWord='Add')
  def _operation(self, x, y):
    return x+y
  def _derivative(self):
    return Addition(self.x1.derivative(),self.x2.derivative())
  def optimize(self):
    if self.x1==Constant(0):
      return self.x2.optimize()
    if self.x2==Constant(0):
      return self.x1.optimize()

class Subtraction(BinaryFunction):
  def __init__(self, x1, x2):
      super(Subtraction, self).__init__(x1, x2, keyWord='Sub')
  def _operation(self, x, y):
    return x-y
  def _derivative(self):
    return Subtraction(self.x1.derivative(),self.x2.derivative())
  def optimize(self):
    if self.x1==Constant(0):
      return self.x2.optimize()
    if self.x2==Constant(0):
      return self.x1.optimize()
    if self.x2==self.x1:
      return Constant(0)

class Multiplication(BinaryFunction):
  def __init__(self, x1, x2):
    super(Multiplication, self).__init__(x1, x2, keyWord='Mult')
  def _operation(self, x, y):
    return x*y
  def _derivative(self):
    return Addition(
      Multiplication(self.x1.derivative(), self.x2),
      Multiplication(self.x1,self.x2.derivative())
      )
  def optimize(self):
    if self.x1==Constant(0) or self.x2==Constant(0):
      return Constant(0)
    if self.x2==Constant(1):
      return self.x1.optimize()
    if self.x1==Constant(1):
      return self.x2.optimize()

class Division(BinaryFunction):
  def __init__(self, x1, x2):
    super(Division, self).__init__(x1, x2, keyWord='Div')
  def _operation(self, x, y):
    return x/y
  def _derivative(self):
    # (f'*g - f*g')/(g^2)
    return\
      Division(
        Subtraction(
          Multiplication(self.x1.derivative(), self.x2),
          Multiplication(self.x1, self.x2.derivative())
        ),
        Power(self.x2, 2)
      )
  def optimize(self):
    if self.x2==Constant(1):
      return self.x1.optimize()
    if self.x1==Constant(1):
      return self.x2.optimize()
    if self.x1==self.x2:
      return Constant(1)

class Power(BinaryFunction):
  def __init__(self, x1, x2):
    super(Power, self).__init__(x1, x2, keyWord='Pow')
  def _operation(self, x, y):
    return x**y
  def _derivative(self):
    # derivative of f^g = (f^g)*((f'*g)/f + ln(f)*g')
    return \
      Multiplication(
        Power(self.x1, self.x2),
        Addition(
          Division(Multiplication(self.x1.derivative(), self.x2), self.x1),
          Multiplication(Logarithm(self.x1, Constant(2.718)), self.x2.derivative()) # TODO
        )
      )
  def optimize(self):
    if self.x2==Constant(1):
      return self.x1.optimize()
    if (self.x1==Constant(1) and self.x2>=Constant(0)) or self.x2==Constant(0):
      return Constant(1)

class Root(BinaryFunction):
  def __init__(self, x1, x2):
    super(Root, self).__init__(x1, x2, keyWord='Root')
  def _operation(self, x, y):
    return x**(1/y)
  def _derivative(self):
    return Power(self.x1, Division(1, self.x2)).derivative()
  def optimize(self):
    if self.x2==Constant(1):
      return self.x1.optimize()
    if self.x2==Constant(0):
      return Constant(1)


class Logarithm(BinaryFunction):
  def __init__(self, x1, x2):
    super(Logarithm, self).__init__(x1, x2, keyWord='Log')
  def _operation(self, x, y):
    return log(x,y)
  def _derivative(self):
    pass # TODO
  def optimize(self):
    if self.x1==self.x2:
      return Constant(1)
  
class Factorial(BinaryFunction):
  def __init__(self, x1):
    super(Factorial, self).__init__(x1, None, keyWord='Fact')
  def _operation(self, x, y):
    return factorial(x)
  def _derivative(self):
    pass # TODO
  def optimize(self):
    if self.x1==Constant(0) or self.x1==Constant(1):
      return Constant(1)

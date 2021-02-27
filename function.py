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

class Variable(IFunction):
  def __init__(self, name):
    self.name = name
  def __str__(self):
    return self.name
  def optimize(self):
    return self
  def derivative(self):
    return Constant(1)

class Constant(IFunction):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)
  def optimize(self):
    return self
  def derivative(self):
    return Constant(0)

class BinaryFunction(IFunction):
  def __init__(self, x1, x2, op, keyWord=''):
    self.x1=x1
    self.x2=x2
    self.op=op
    self.keyWord = keyWord

  def __str__(self):
    return self.keyWord+'('+str(self.x1)+', '+str(self.x2)+')'

  def __eq__(self, f2):
    return str(self) == str(f2)

  def getVariables(self):
    vars=[]
    for x in (self.x1,self.x2):
      if isinstance(x, Variable) and x not in vars:
          vars.append(x.name)
      elif isinstance(x, BinaryFunction):
        for v in x.getVariables():
          if v not in vars:
            vars.append(v)
    return vars


  def derivative(self):
    if len(self.getVariables()) > 1:
      print("Only functions with at most one variable can be derived at this time")
      return
    return self._derivative()
  
  def _derivative(self):
    pass
  
  def _getValue(self, x, coords):
    if isinstance(x, Variable): return coords[x.name]
    elif isinstance(x, BinaryFunction): return x.doOperation(coords)
    elif isinstance(x, Constant): return x.value
    else: return None

  def doOperation(self,coords):
    v1=self._getValue(self.x1, coords)
    v2=self._getValue(self.x2, coords)
    return self.op(v1, v2)

  def optimize(self):
    pass

class Identity(BinaryFunction):
  def __init__(self, x1):
    super(Identity, self).__init__(x1, None, lambda x,y: x, keyWord='Id')
  def _derivative(self):
    return Identity(self.x1.derivative())
  def optimize(self):
    return self.x1.optimize()
  
class Addition(BinaryFunction):
  def __init__(self, x1, x2):
    super(Addition, self).__init__(x1, x2, lambda x,y: x+y, keyWord='Add')
  def _derivative(self):
    return Addition(self.x1.derivative(),self.x2.derivative())
  def optimize(self):
    if self.x1==Constant(0):
      return self.x2.optimize()
    if self.x2==Constant(0):
      return self.x1.optimize()

class Subtraction(BinaryFunction):
  def __init__(self, x1, x2):
      super(Subtraction, self).__init__(x1, x2, lambda x,y: x-y, keyWord='Sub')
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
    super(Multiplication, self).__init__(x1, x2, lambda x,y: x*y, keyWord='Mult')
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
    super(Division, self).__init__(x1, x2, lambda x,y: x/y, keyWord='Div')
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
    super(Power, self).__init__(x1, x2, lambda x,y: x**y, keyWord='Pow')
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
    super(Root, self).__init__(x1, x2, lambda x,y: x**(1/y), keyWord='Root')
  def _derivative(self):
    return Power(self.x1, Division(1, self.x2)).derivative()
  def optimize(self):
    if self.x2==Constant(1):
      return self.x1.optimize()
    if self.x2==Constant(0):
      return Constant(1)


class Logarithm(BinaryFunction):
  def __init__(self, x1, x2):
    super(Logarithm, self).__init__(x1, x2, log, keyWord='Log')
  def _derivative(self):
    pass # TODO
  def optimize(self):
    if self.x1==self.x2:
      return Constant(1)
  
class Factorial(BinaryFunction):
  def __init__(self, x1):
    super(Factorial, self).__init__(x1, None, lambda x,y: factorial(x), keyWord='Fact')
  def _derivative(self):
    pass # TODO
  def optimize(self):
    if self.x1==Constant(0) or self.x1==Constant(1):
      return Constant(1)

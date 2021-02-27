from math import log
from utils import factorial

"""
TODO
recursive call for optimize
"""

class Variable:
  def __init__(self, name):
    self.name = name
  def __eq__(self, v2):
    return self.name == v2.name

class BinaryFunction:
  def __init__(self, x1, x2, op):
    self.x1=x1
    self.x2=x2
    self.op=op

  def __str__(self,):
    s = str(self.x1)+' '+str(self.x2)+' '+str(self.op)
    return s

  def getVariables(self):
    vars=[]
    for x in (self.x1,self.x2):
      if isinstance(x, Variable): vars.append(x.name)
      elif isinstance(x, BinaryFunction): vars += x.getVariables()
    return vars

  def _getValue(self, x, coords):
    if isinstance(x, Variable): return coords[x.name]
    elif isinstance(x, BinaryFunction): return x.doOperation(coords)
    else: return x
  
  def doOperation(self,coords):
    v1=self._getValue(self.x1, coords)
    v2=self._getValue(self.x2, coords)
    return self.op(v1, v2)

  def optimize(self):
    pass

class Identity(BinaryFunction):
  def __init__(self, x1):
    super(Identity, self).__init__(x1, None, lambda x,y: x)
  def optimize(self):
    return self.x1

class Addition(BinaryFunction):
  def __init__(self, x1, x2):
    super(Addition, self).__init__(x1, x2, lambda x,y: x+y)
  def optimize(self):
    if self.x1==0:
      return self.x2
    if self.x2==0:
      return self.x1

class Subtraction(BinaryFunction):
  def __init__(self, x1, x2):
    super(Subtraction, self).__init__(x1, x2, lambda x,y: x-y)
  def optimize(self):
    if self.x1==0:
      return self.x2
    if self.x2==0:
      return self.x1
    if self.x2==self.x1:
      return 0

class Multiplication(BinaryFunction):
  def __init__(self, x1, x2):
    super(Multiplication, self).__init__(x1, x2, lambda x,y: x*y)
  def optimize(self):
    if self.x1==0 or self.x2==0:
      return 0
    if self.x2==1:
      return self.x1
    if self.x1==1:
      return self.x2

class Division(BinaryFunction):
  def __init__(self, x1, x2):
    super(Division, self).__init__(x1, x2, lambda x,y: x/y)
  def optimize(self):
    if self.x2==1:
      return self.x1
    if self.x1==1:
      return self.x2
    if self.x1==self.x2:
      return 1

class Power(BinaryFunction):
  def __init__(self, x1, x2):
    super(Power, self).__init__(x1, x2, lambda x,y: x**y)
  def optimize(self):
    if self.x2==1:
      return self.x1
    if (self.x1==1 and self.x2>=0) or self.x2==0:
      return 1

class Root(BinaryFunction):
  def __init__(self, x1, x2):
    super(Root, self).__init__(x1, x2, lambda x,y: x**(1/y))
  def optimize(self):
    if self.x2==1:
      return self.x1
    if self.x2==0:
      return 1


class Logarithm(BinaryFunction):
  def __init__(self, x1, x2):
    super(Logarithm, self).__init__(x1, x2, log)
  def optimize(self):
    if self.x1==self.x2:
      return 1
  

class Factorial(BinaryFunction):
  def __init__(self, x1):
    super(Factorial, self).__init__(x1, None, lambda x,y: factorial(x))
  def optimize(self):
    if self.x1==0 or self.x1==1:
      return 1
  
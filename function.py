from math import log
from utils import factorial

class Variable:
  def __init__(self, name):
    self.name = name
  def __str__(self):
    return self.name

class BinaryFunction:
  def __init__(self, x1, x2, op):
    self.x1=x1
    self.x2=x2
    self.op=op

  def __str__(self,):
    #s = str(self.x1)+' '+str(self.x2)+' '+str(self.op)
    s = self._getStr()+'('+str(self.x1)+', '+str(self.x2)+')'
    return s
  def __eq__(self, f2):
    return str(self) == str(f2)

  def getVariables(self):
    vars=[]
    for x in (self.x1,self.x2):
      if isinstance(x, Variable): vars.append(x.name)
      elif isinstance(x, BinaryFunction): vars += x.getVariables()
    return vars

  def _derivative(self):
     pass
  
  def _getStr(self):
    pass

  def _getValue(self, x, coords):
    if isinstance(x, Variable): return coords[x.name]
    elif isinstance(x, BinaryFunction): return x.doOperation(coords)
    else: return x

  def _getDerivative(self, x):
    if isinstance(x, Variable): return 1
    elif isinstance(x, BinaryFunction): return x._derivative()
    else: return 0

  def doOperation(self,coords):
    v1=self._getValue(self.x1, coords)
    v2=self._getValue(self.x2, coords)
    return self.op(v1, v2)

class Identity(BinaryFunction):
  def __init__(self, x1):
    super(Identity, self).__init__(x1, None, lambda x,y: x)
  def _derivative(self):
    return Identity(self._getDerivative(self.x1))
  def _getStr(self):
    return 'Id'

class Addition(BinaryFunction):
  def __init__(self, x1, x2):
    super(Addition, self).__init__(x1, x2, lambda x,y: x+y)
  def _derivative(self):
    return Addition(self._getDerivative(self.x1),self._getDerivative(self.x2))
  def _getStr(self):
    return 'Add'

class Subtraction(BinaryFunction):
  def __init__(self, x1, x2):
      super(Subtraction, self).__init__(x1, x2, lambda x,y: x-y)
  def _derivative(self):
    return Subtraction(self._getDerivative(self.x1),self._getDerivative(self.x2))
  def _getStr(self):
    return 'Sub'


class Multiplication(BinaryFunction):
  def __init__(self, x1, x2):
    super(Multiplication, self).__init__(x1, x2, lambda x,y: x*y)
  def _derivative(self):
    return Addition(
      Multiplication(self._getDerivative(self.x1), self.x2),
      Multiplication(self.x1,self._getDerivative(self.x2))
      )
  def _getStr(self):
    return 'Mult'


class Division(BinaryFunction):
  def __init__(self, x1, x2):
    super(Division, self).__init__(x1, x2, lambda x,y: x/y)
  def _derivative(self):
    # (f'*g - f*g')/(g^2)
    return\
      Division(
        Subtraction(
          Multiplication(self._getDerivative(self.x1), self.x2),
          Multiplication(self.x1, self._getDerivative(self.x2))
        ),
        Power(self.x2, 2)
      )
  def _getStr(self):
    return 'Div'


class Power(BinaryFunction):
  def __init__(self, x1, x2):
    super(Power, self).__init__(x1, x2, lambda x,y: x**y)
  def _derivative(self):
    # (f^g)*((f'*g)/f + ln(f)*g')
    return \
      Multiplication(
        Power(self.x1, self.x2),
        Addition(
          Division(Multiplication(self._getDerivative(self.x1), self.x2), self.x1),
          Multiplication(Logarithm(self.x1, 2.718), self._getDerivative(self.x2)) # TODO
        )
      )
  def _getStr(self):
    return 'Pow'


class Root(BinaryFunction):
  def __init__(self, x1, x2):
    super(Root, self).__init__(x1, x2, lambda x,y: x**(1/y))
  def _derivative(self):
    return Power(self.x1, Division(1, self.x2))._derivative()
  def _getStr(self):
    return 'Root'


class Logarithm(BinaryFunction):
  def __init__(self, x1, x2):
    super(Logarithm, self).__init__(x1, x2, log)
  def _derivative(self):
    pass
  def _getStr(self):
    return 'Log'


class Factorial(BinaryFunction):
  def __init__(self, x1):
    super(Factorial, self).__init__(x1, None, lambda x,y: factorial(x))
  def _derivative(self):
    pass
  def _getStr(self):
    return 'Fact'
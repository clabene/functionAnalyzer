class Variable:
  def __init__(self, name):
    self.name = name

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

class Identity(BinaryFunction):
  def __init__(self, x1):
    super(Identity, self).__init__(x1, None, lambda x,y: x)

class Addition(BinaryFunction):
  def __init__(self, x1, x2):
    super(Addition, self).__init__(x1, x2, lambda x,y: x+y)

class Subtraction(BinaryFunction):
  def __init__(self, x1, x2):
      super(Subtraction, self).__init__(x1, x2, lambda x,y: x-y)

class Multiplication(BinaryFunction):
  def __init__(self, x1, x2):
    super(Multiplication, self).__init__(x1, x2, lambda x,y: x*y)

class Division(BinaryFunction):
  def __init__(self, x1, x2):
    super(Division, self).__init__(x1, x2, lambda x,y: x/y)

class Power(BinaryFunction):
  def __init__(self, x1, x2):
    super(Power, self).__init__(x1, x2, lambda x,y: x**y)

class Root(BinaryFunction):
  def __init__(self, x1, x2):
    super(Root, self).__init__(x1, x2, lambda x,y: x**(1/y))

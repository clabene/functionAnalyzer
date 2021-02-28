from iTest import ITest
import function as F
import random as rand

class FullDerivativeTest(ITest):
  def generateData(self):
    return [
      {"expected":F.Addition(F.Constant(1), F.Constant(1)), "f":F.Addition(F.Variable('x'), F.Variable('x'))},
      {"expected":F.Identity(F.Constant(1)), "f":F.Identity(F.Variable('x'))},
      {"expected":
          F.Multiplication(
            F.Power(F.Variable('x'), F.Constant(2)),
            F.Addition(
              F.Division(
                F.Multiplication(F.Constant(1), F.Constant(2)),
                F.Variable('x')
              ),
              F.Multiplication(
                F.Logarithm(F.Variable('x'), F.Constant(2.718)),
                F.Constant(0)
              )
            )
          ),
        "f":F.Power(F.Variable('x'), F.Constant(2))},
    ]
  def test(self, expected, f):
    der = f.derivative()
    assert expected == der, f'expected {expected}, but got {der} for {f}'

class EqualityDerivativeTest(ITest):
  def generateData(self):
    return [
      {"expected":F.Multiplication(F.Variable('x'), F.Constant(2)), "f":F.Power(F.Variable('x'), F.Constant(2)), "rng":[(1,100)], "N":1_000},
    ]

  def test(self, expected, f, rng, N):
    vars = [v.name for v in f.getVariables()]
    samplePoint = lambda : [rand.random()*(xmax-xmin)+xmin for xmin,xmax in rng]
    sampledPoints = [samplePoint() for _ in range(N)]

    der = f.derivative()
    
    for x in sampledPoints:
      params = dict(zip(vars, x))
      d = der.operation(params)
      e = expected.operation(params)
      assert abs(d-e)<1E-5, f"expected {e}, got {d} for {x}"
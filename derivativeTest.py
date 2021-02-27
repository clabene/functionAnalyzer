from iTest import ITest
import function as F

class DerivativeTest(ITest):
  def generateData(self):
    return [
      {"expected":F.Addition(1,1), "f":F.Addition(F.Variable('x'), F.Variable('x'))},
      {"expected":F.Identity(1), "f":F.Identity(F.Variable('y'))},
      {"expected":F.Multiplication(2, F.Variable('y')), "f":F.Power(F.Variable('y'), 2)},
    ]
  def test(self, expected, f):
    der = f._derivative()
    print(der)
    print(expected)
    print()
    assert expected == der, f'expected {expected} but got {der}'
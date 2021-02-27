from iTest import ITest
import function as F

class OptimizeTest(ITest):
  data = [
    {"expected":0, "func":F.Multiplication(0, 3)},
  ]
  def generateData(self):
    return OptimizeTest.data
  def test(self, expected, func):
    opt = func.optimize()
    assert expected == opt, f"Error: expected: {expected}, but got: {opt} for {func}"
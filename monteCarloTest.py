"""
Per più integrali:
https://www.youmath.it/esercizi/es-analisi-matematica/es-sugli-integrali/3305-esercizi-integrali-elementari.html
"""
from iTest import ITest

from monteCarlo import monteCarlo
from functionParser import getFunction

class MonteCarloWithSolutionTest(ITest):
  data = [
    {"expected":50,"expr":"x","inRanges":[(0,10)],"outRange":(0,100),"N":None,},
    {"expected":3.14159265358979323846,"expr":"PI","inRanges":[],"outRange":(0,5),"N":None,},
    {"expected":3*5,"expr":"3","inRanges":[(0,5)],"outRange":(0,5),"N":None,},
  ]
  def generateData(self):
    return MonteCarloWithSolutionTest.data
  def test(self, expected, expr, inRanges, outRange, N=None, tollerance=0.1):
    fun = getFunction(expr)
    vol=monteCarlo(fun, inRanges=inRanges, outRange=outRange, N=N)
    assert (vol-expected) < vol*tollerance, f"volume of {expr} on input space {inRanges} is off by {vol-expected}"  


class MonteCarloWithIntegralTest(ITest):
  data = [
    {"integral":"(x^2)/2","expr":"x","inRanges":[(0,10)],"outRange":(0,100),"N":None,},
    {"integral":"(x^4)/8","expr":"(x^3)/2","inRanges":[(0,10)],"outRange":(0,10_000),"N":None,},
    {"integral":"2*lg(x,E)","expr":"2/x","inRanges":[(5,15)],"outRange":(0,1),"N":100_000,},
  ]
  def generateData(self):
    return MonteCarloWithIntegralTest.data
  def test(self, integral, expr, inRanges, outRange, N=None, tollerance=0.1):
    fun = getFunction(expr)
    vol=monteCarlo(fun, inRanges=inRanges, outRange=outRange, N=N)
    
    fun_i = getFunction(integral)
    vars_i = [v.name for v in fun_i.getVariables()]
    v1 = fun_i.operation(
      coords=dict(zip(vars_i, [r for _,r in inRanges] ))
    )
    v0 = fun_i.operation(
      coords=dict(zip(vars_i, [l for l,_ in inRanges] ))
    )
    expected = v1-v0
    assert (vol-expected) < vol*tollerance, f"volume of {expr} on input space {inRanges} is off by {vol-expected}"
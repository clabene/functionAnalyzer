"""
Per più integrali:
https://www.youmath.it/esercizi/es-analisi-matematica/es-sugli-integrali/3305-esercizi-integrali-elementari.html
"""

from monteCarlo import monteCarlo
from functionParser import getFunction

def testWithSolution(expected, expr, inRanges, outRange, N=None, tollerance=0.1):
  fun = getFunction(expr)
  vol=monteCarlo(fun, inRanges=inRanges, outRange=outRange, N=N)
  # print("% 7f % 7f"%(abs(vol-expected), vol*tollerance), (vol-expected) < vol*tollerance)
  assert (vol-expected) < vol*tollerance, f"volume of {expr} on input space {inRanges} is off by {vol-expected}"

def testWithIntegral(integral, expr, inRanges, outRange, N=None, tollerance=0.1):
  fun = getFunction(expr)
  fun_i = getFunction(integral)
  vol=monteCarlo(fun, inRanges=inRanges, outRange=outRange, N=N)
  v1 = fun_i.doOperation(
    coords=dict(zip(fun_i.getVariables(), [r for _,r in inRanges] ))
  )
  v0 = fun_i.doOperation(
    coords=dict(zip(fun_i.getVariables(), [l for l,_ in inRanges] ))
  )
  expected = v1-v0
  # print("% 7f % 7f"%(abs(vol-expected), vol*tollerance), abs(vol-expected) < vol*tollerance)
  assert (vol-expected) < vol*tollerance, f"volume of {expr} on input space {inRanges} is off by {vol-expected}"

withSolution = [
  {"expected":50,"expr":"x","inRanges":[(0,10)],"outRange":(0,100),"N":None,},
  {"expected":3.14159265358979323846,"expr":"PI","inRanges":[],"outRange":(0,5),"N":None,},
  {"expected":3*5,"expr":"3","inRanges":[(0,5)],"outRange":(0,5),"N":None,},
]

withIntegrals = [
  {"integral":"(x^2)/2","expr":"x","inRanges":[(0,10)],"outRange":(0,100),"N":None,},
  {"integral":"(x^4)/8","expr":"(x^3)/2","inRanges":[(0,10)],"outRange":(0,10_000),"N":None,},
  {"integral":"2*lg(x,E)","expr":"2/x","inRanges":[(5,15)],"outRange":(0,1),"N":None,},
]

for d in withSolution: testWithSolution(**d)
for d in withIntegrals: testWithIntegral(**d)
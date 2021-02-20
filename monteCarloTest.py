"""
Integrali presi da
https://www.youmath.it/esercizi/es-analisi-matematica/es-sugli-integrali/3305-esercizi-integrali-elementari.html
"""

from monteCarlo import monteCarlo
from functionParser import getFunction

def testWithExpected(expected, expr, inRanges, outRange, N=None):
  fun = getFunction(expr)
  vol=monteCarlo(fun, inRanges=inRanges, outRange=outRange, N=N)
  print(vol, expected, abs(vol-expected), vol-expected)
  #assert (vol-expected) < vol*0.1

def testWithIntegral(integral, expr, inRanges, outRange, N=None):
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
  print(vol, expected, abs(vol-expected), vol-expected)
  #assert (vol-expected) < vol*0.1

withSolution = [
  {"expected":50,"expr":"x","inRanges":[(0,10)],"outRange":(0,100),"N":None,},
]

withIntegrals = [
  {"integral":"(x^2)/2","expr":"x","inRanges":[(0,10)],"outRange":(0,100),"N":None,},
  {"integral":"(x^4)/8","expr":"(x^3)/2","inRanges":[(0,10)],"outRange":(0,10_000),"N":None,},
]


for d in withIntegrals: testWithIntegral(**d)
import random as rand
from functionParser import getFunction


def monteCarlo(fun, inRanges, outRange, N=None):
  vars = fun.getVariables()
  assert len(inRanges) == len(vars)
  D=len(vars) # input dimensionality (nr of variables)
  ranges=inRanges+[outRange] # sampling space
  V = 1 # volume of sampling region
  for xmin,xmax in ranges:
    V*=(xmax-xmin)
  if not N: N=V*20 # nr samples to draw
  samplePoint = lambda : [rand.random()*(xmax-xmin)+xmin for xmin,xmax in ranges] # random point in D+1 dimensions within the sampling region
  sampledPoints = [samplePoint() for _ in range(N)] # randomly sampled points
  ratio = sum(fun.doOperation(dict(zip(vars, x[:-1])))>=x[-1] for x in sampledPoints) # number of points randomly drawn below the function
  ratio/=N # percentage of points drawn below the function
  ratio*=V # approximation of percentage of sampling region below the function
  return ratio

if __name__=="__main__":
  expr = "3*x^2"
  f=getFunction(expr)
  inRanges = [(0,10)]
  outRange = (0,300)
  N=1_000_000
  vol=monteCarlo(f, inRanges=inRanges, outRange=outRange, N=N)
  print(vol)

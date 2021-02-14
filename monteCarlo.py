import random as rand
from functionParser import getFunction

expr = "3*x^2+y"
f=getFunction(expr)
vars = f.getVariables()

D = len(vars) # input dimensionality (nr of variables)
inRanges=[] # sampling ranges in the input space
for _ in range(D):
  inRanges.append((5,12))
outRange = (0,2_000) # sampling ranges in the output space
ranges = inRanges+[outRange] # sampling space

V = 1 # volume of sampling region
for xmin,xmax in ranges:
  V*=(xmax-xmin)

#N=1_000_000 # nr of samples to draw
N=V*10 # nr of samples to draw

samplePoint = lambda : [rand.random()*(xmax-xmin)+xmin for xmin,xmax in ranges] # random point in D+1 dimensions within the sampling region
sampledPoints = [samplePoint() for _ in range(N)] # randomly sampled points
ratio = sum(f.doOperation(dict(zip(vars, x[:-1])))>=x[-1] for x in sampledPoints) # number of points randomly drawn below the function
ratio/=N # percentage of points drawn below the function
ratio*=V # approximation of percentage of sampling region below the function
print(ratio)

"""
xmin, xmax = 5,12
ymin, ymax = 0,2_000
V = (ymax-ymin)*(xmax-xmin)
N = 1_000_000

sample_points = [(rand.random()*(xmax-xmin)+xmin, rand.random()*(ymax-ymin)+ymin) for _ in range(N)]

ratio = sum(f.doOperation({'x':x_i})>=y_i for x_i,y_i in sample_points)/N
print(ratio*V)
"""

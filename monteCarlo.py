import random as rand

from function import Function as F

f = F()

xmin, xmax = 5,12
ymin, ymax = 0,1_000
V = (ymax-ymin)*(xmax-xmin)
N = 1_000_000

sample_points = [(rand.random()*(xmax-xmin), rand.random()*(ymax-ymin)) for _ in range(N)]

ratio = sum(f(x_i)>=y_i for x_i,y_i in sample_points)/N
print(ratio*V)

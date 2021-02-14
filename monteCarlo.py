import random as rand
from functionParser import getFunction

expr = "3*x^2"
f=getFunction(expr)

xmin, xmax = 5,12
ymin, ymax = 0,2_000
V = (ymax-ymin)*(xmax-xmin)
N = 1_000_000

sample_points = [(rand.random()*(xmax-xmin)+xmin, rand.random()*(ymax-ymin)+ymin) for _ in range(N)]

ratio = sum(f.doOperation({'x':x_i})>=y_i for x_i,y_i in sample_points)/N
print(ratio*V)

fi = getFunction("x^3")
print(fi.doOperation({'x':xmax})-fi.doOperation({'x':xmin}))

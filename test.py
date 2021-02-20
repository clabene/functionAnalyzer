from functionParser import getFunction
import math

def test(expr, coords, expected):
  f=getFunction(expr)
  res = f.doOperation(coords=coords)
  assert (expected == res), \
    "expr: %s, expected: %f, actual: %f"%(expr, expected, res)

ds=[
  {"expr":"10.2", "coords":{}, "expected":10.2},
  {"expr":"10^2", "coords":{}, "expected":100},
  {"expr":"2+3*3+4", "coords":{}, "expected":15},
  {"expr":"2.0+3*3.0+4.0", "coords":{}, "expected":15},
  {"expr":"4|2", "coords":{}, "expected":2},
  {"expr":"-12*3", "coords":{"x":2},"expected":-36,},
  {"expr":"4|2*5", "coords":{}, "expected":10},
  {"expr":"100|(1+1)", "coords":{}, "expected":10},
  {"expr":"16|2*5", "coords":{}, "expected":20},
  {"expr":"10+((3*22^2+1*2+(1+2^2*(10+2*3)))*(22+8*1))", "coords":{},
    "expected":10+((3*(22**2)+1*2+(1+(2**2)*(10+2*3)))*(22+8*1))},

  {"expr":"x", "coords":{"x":1}, "expected":1,},
  {"expr":"x+3", "coords":{"x":5}, "expected":8,},
  {"expr":"x^3", "coords":{"x":3}, "expected":27,},
  {"expr":"x|2", "coords":{"x":100}, "expected":10,},
  {"expr":"100|x", "coords":{"x":2}, "expected":10,},
  {"expr":"10*((2*x)^2)", "coords":{"x":3}, "expected":360,},

  {"expr":"x+y", "coords":{"x":5, "y":2}, "expected":7,},
  {"expr":"7+x^2*y^2", "coords":{"x":2, "y":4}, "expected":71,},
  {"expr":"x*y", "coords":{"x":4, "y":2}, "expected":8,},
  {"expr":"x|y", "coords":{"x":16, "y":2}, "expected":4,},

  {"expr":"x+y/z", "coords":{"x":10, "y":4, "z":2}, "expected":12,},
  {"expr":"x+y/z^2-22", "coords":{"x":11, "y":24, "z":2}, "expected":-5,},

  {"expr":"pw(2,3)", "coords":{}, "expected":8,},
  {"expr":"pw(x,3)", "coords":{"x":5}, "expected":125,},
  {"expr":"rt(pw(x,6),6)", "coords":{"x":5}, "expected":5,},
  {"expr":"lg(8,x)", "coords":{"x":2}, "expected":3,},
  {"expr":"pw(2,pw(2,2))", "coords":{"x":2}, "expected":16,},
  {"expr":"pw(lg(8,x), rt(16,x))", "coords":{"x":2},
    "expected":math.log(8,2)**(16**(1/2)),},

  {"expr":"100-pw(lg(8,x)-1, rt(16,x))", "coords":{"x":2},
    "expected":100-( (math.log(8,2)-1)**(16**(1/2)) ),},
    {"expr":"-pw(lg(8,x)-1, rt(16.0,x))", "coords":{"x":2},
      "expected":-( (math.log(8,2)-1)**(16**(1/2)) ),},

  {"expr":"PI+E", "coords":{},
    "expected":3.14159265358979323846+2.71828182845904523536,},

  {"expr":"5!", "coords":{}, "expected":120,},
  {"expr":"3+5!", "coords":{}, "expected":123,},
  {"expr":"3*3!", "coords":{}, "expected":18,},
  {"expr":"3*x!", "coords":{'x':4.2}, "expected":72,},
  {"expr":"(3+x)!*2", "coords":{'x':2}, "expected":240,},
  {"expr":"pw((3+x)!,3*2)", "coords":{'x':2.9}, "expected":120**6,},
  {"expr":"pw((3+x)!,3*2)", "coords":{'x':-4}, "expected":1,},


]

for d in ds: test(**d)

import re

PATTERN_PAR = '\([^\(\)]*\)'
PATTERN_PH = '_[0-9]+_'

OPERANDS = list("+-*/^|!") # TODO reaname OPERATIONS
KEYWORDS = ['rt', 'pw', 'lg']

def getPattern(operands, pairnOnly=False):
  excludedStr = '\\'+'\\'.join(o for o in OPERANDS if (o not in operands or pairnOnly))
  selectedStr = '\\'+'\\'.join(o for o in operands)
  return f"[^{excludedStr}]+[{selectedStr}][^{excludedStr}]+"

class SubstringFinder:
  def find(self, s):
    pass

class AddSubFinder(SubstringFinder):
  def find(self, s):
    pattern = getPattern(["+","-"], True)
    return [(m.start(0), m.end(0)) for m in re.finditer(pattern, s)]

class MultDivFinder(SubstringFinder):
  def find(self, s):
    pattern = getPattern(["*","/"], True)
    return [(m.start(0), m.end(0)) for m in re.finditer(pattern, s)]

class PowRootFinder(SubstringFinder):
  def find(self, s):
    pattern = getPattern(["^","|"], True)
    return [(m.start(0), m.end(0)) for m in re.finditer(pattern, s)]
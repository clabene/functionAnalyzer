import re

import function as F
from utils import mergeDict, decompose

PATTERN_PAR = '\([^\(\)]*\)' # 2+2+12*(1*(2/3)+2)+11 -> (2/3)
PATTERN_PH = '_[0-9]+_'

OPERANDS = list("+-*/^|") # TODO reaname OPERATIONS
KEYWORDS = ['rt', 'pw', 'lg']

def getPattern(operands, pairnOnly=False):
  excludedStr = '\\'+'\\'.join(o for o in OPERANDS if (o not in operands or pairnOnly))
  selectedStr = '\\'+'\\'.join(o for o in operands)
  return f"[^{excludedStr}]+[{selectedStr}][^{excludedStr}]+"

def findInnerParenthesisRE(expr):
  pattern = '(?<!'+'|'.join(KEYWORDS)+')'+PATTERN_PAR # all parenthesis that are not preceded by a keyword
  return [(m.start(0), m.end(0)) for m in re.finditer(pattern, expr)]

def extractPlaceHolderRE(expr):
  return re.findall(PATTERN_PH, expr)

def findAddSubRE(expr):
  pattern = getPattern(["+","-"], True)
  return [(m.start(0), m.end(0)) for m in re.finditer(pattern, expr)]

def findMultDivRE(expr):
  pattern = getPattern(["*","/"], True)
  return [(m.start(0), m.end(0)) for m in re.finditer(pattern, expr)]

def findPowRootRE(expr):
  pattern = getPattern(["^","|"], True)
  return [(m.start(0), m.end(0)) for m in re.finditer(pattern, expr)]

def findKeyWordsRE(expr):
  idxs=[]
  for keyword in KEYWORDS:
    pattern = keyword+PATTERN_PAR
    idxs += [(m.start(0), m.end(0)) for m in re.finditer(pattern, expr)]
  return idxs

def findKeyWordsArgsRE(expr):
  pattern = "\(.*["+'\\'+'\\'.join(OPERANDS)+"].*\,"
  idxs = [(m.start(0)+1, m.end(0)-1) for m in re.finditer(pattern, expr)]
  pattern = "\,.*["+'\\'+'\\'.join(OPERANDS)+"].*\)"
  idxs= idxs+[(m.start(0)+1, m.end(0)-1) for m in re.finditer(pattern, expr)]
  return idxs

"""
2+3*4^(3+1) -> 2+_2_, {_0_: 3+1, _1_: 4^_0_, _2_: 3*_1_}
"""
def tokenize(expr, placeHolder=0):
  expr, tokens = decompose(expr, findInnerParenthesisRE)
  for k in tokens:
    tokens[k] = tokens[k][1:-1] # remove parehtesis
  for idxFinder in [findKeyWordsRE, findKeyWordsArgsRE, findPowRootRE, findMultDivRE, findAddSubRE]:
    expr, newTokens = decompose(expr, idxFinder, placeHolder+len(tokens.keys()))
    tokens = mergeDict(tokens, newTokens)
  return expr, tokens

"""
Tree representation of a tokenized expression
2+(3*4+1)^(3+1)
->
    2+_2_
       /
    _0_^_1_
     /    \
   _2_+1  3+1
    /
   3*4
"""
class ExpressionTree:
  def __init__(self, expr, tokens={}, placeHolder=0):
    self.expr, newTokens = tokenize(expr, placeHolder)
    tokens = mergeDict(tokens, newTokens)
    self.tokens = {}
    tokenKeys = extractPlaceHolderRE(self.expr)
    for k in tokenKeys:
      self.tokens[k] = ExpressionTree(tokens[k], tokens, placeHolder=placeHolder+len(tokens))

  def __str__(self):
    s=self.expr
    for k in self.tokens:
      s=s.replace(k, '('+str(self.tokens[k])+')')
    return s

  def printTree(self, indent=""):
    print(indent+"-"*10)
    print(indent+"Value ", self.expr)
    print(indent+f"{len(self.tokens.keys())} children.")
    for k in self.tokens:
      print(indent+k)
      self.tokens[k].printTree(indent=indent+"   ")

def isNumber(s):
  try: float(s)
  except: return False
  return True

isPlaceHolder = lambda s: len(s)>2 and s[0]==s[-1]=='_' and all(c.isdigit() for c in s[1:-1])
isVariable    = lambda s: not (isNumber(s) or isPlaceHolder(s) or isKeyWord(s) or any(c in s for c in OPERANDS))
isUnit        = lambda s: isNumber(s) or isVariable(s)
isKeyWord     = lambda s: any(s[:2]==k for k in KEYWORDS)
isSum         = lambda s: '+' in s
isSub         = lambda s: '-' in s
isMult        = lambda s: '*' in s
isDiv         = lambda s: '/' in s
isPow         = lambda s: '^' in s
isRoot        = lambda s: '|' in s

def parseUnit(element):
  if isNumber(element):
    return float(element)
  elif isVariable(element):
    return F.Variable(name=element)

def treeToFunction(tree):
  if isUnit(tree.expr): return F.Identity(parseUnit(tree.expr))

  if isPlaceHolder(tree.expr): return treeToFunction(tree.tokens[tree.expr])

  if isKeyWord(tree.expr):
    fun = tree.expr[:2]
    operands=[parseUnit(o) if isUnit(o) else treeToFunction(tree.tokens[o]) for o in tree.expr[3:-1].split(',')]
    if   fun=='lg': return F.Logarithm(*operands)
    elif fun=='pw': return F.Power(*operands)
    elif fun=='rt': return F.Root(*operands)

  if isSum(tree.expr):
    symbol='+'
    funct = F.Addition
  elif isSub(tree.expr):
    symbol='-'
    funct = F.Subtraction
  elif isMult(tree.expr):
    symbol='*'
    funct = F.Multiplication
  elif isDiv(tree.expr):
    symbol='/'
    funct = F.Division
  elif isPow(tree.expr):
    symbol='^'
    funct = F.Power
  elif isRoot(tree.expr):
    symbol='|'
    funct = F.Root
  operands=[parseUnit(o) if isUnit(o) else treeToFunction(tree.tokens[o]) for o in tree.expr.split(symbol)]
  return funct(*operands)

def getFunction(expr):
  if expr[0]=='-': expr='0'+expr
  expr=expr.replace(' ','')
  return treeToFunction(ExpressionTree(expr))

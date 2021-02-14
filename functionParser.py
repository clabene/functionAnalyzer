import re

import function as f

"""
PATTERN_MUL_DIV_PAIR = '[^\^\+\-\*/|]+[\*\/][^\^\+\-\*/|]+'
# 2+52/18 -> 52/18
# 2+2+12*12+2 -> 12*12
# 2+2+12*12*12+2 -> 12*12
# 2+2+12*12/3+2 -> 12*12

PATTERN_MUL_DIV = '[^\^\+\-\|]+[\*\/][^\^\+\-/|]+'
# 2+52/18 -> 52/18
# 2+2+12*12+2 -> 12*12
# 2+2+12*12*12+2 -> 12*12*12
# 2+2+12*12/3+2 -> 12*12/3
"""

PATTERN_PAR = '\([^\(\)]+\)'
# 2+2+12*(1*(2/3)+2)+11 -> (2/3)
# 2+2+12*(1*2/3+2)+11 -> (1*2/3+2)

PATTERN_PH = '_[0-9]+_'

OPERANDS = list("+-*/^|") # TODO reaname OPERATIONS

def getPattern(operands, pairnOnly=False):
  excludedStr = '\\'+'\\'.join(o for o in OPERANDS if (o not in operands or pairnOnly))
  selectedStr = '\\'+'\\'.join(o for o in operands)
  return f"[^{excludedStr}]+[{selectedStr}][^{excludedStr}]+"

def mergeDict(d1, d2):
  return dict(d1, **d2)

"""
Rerturns the indices of all parenthesis that have no inner parenthesis
2+(1+(2+3)+(2*3)) -> [(5,10), (11,16)]
"""
def findInnerParenthesis(expr):
  idxs = []
  openIdx=-1
  for i,c in enumerate(expr):
    if c == '(':
      openIdx = i
    elif c == ')' and openIdx!=-1:
      idxs.append((openIdx, i))
      openIdx=-1
  return idxs

def findInnerParenthesisRE(expr):
  return [(m.start(0), m.end(0)) for m in re.finditer(PATTERN_PAR, expr)]

def findPlaceHolderRE(expr):
  return [(m.start(0), m.end(0)) for m in re.finditer(PATTERN_PH, expr)]

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

def findOperationRE(expr):
  pattern = getPattern(OPERANDS, True)
  return [(m.start(0), m.end(0)) for m in re.finditer(pattern, expr)]

"""
ciao come va, [(5,9)] -> ciao _0_ va, {_0_:come}
(2+3)+(5+6)+1, [(0,5), (6,10)] -> _0_+_1_+1, {_0_:(2+3), _1_:(5+6)}
(2+3)+(5+6)+1, [(0,5), (6,10)], 10 -> _10_+_11_+1, _10_:(2+3), _11_:(5+6)
"""
def breakDownExpr(expr, idxs, placeHolder=0):
  idxs.sort(key=lambda x: -x[0])
  subExprs={}
  for i,(l,r) in enumerate(idxs):
    ID = "_%d_"%(placeHolder + len(idxs)-1-i)
    subExprs[ID] = expr[l:r]
    expr = expr[:l]+ID+expr[r:]
  return expr, subExprs
"""
1+(2+3)+(2*3+(8+4)) -> 1+_0_+_2_, {'_0_': '2+3', '_1_': '8+4', '_2_': '2*3+_1_'}
"""
# expr -> string to tokenize
# idxFinder -> function that finds indices iteratively
def iterativeBreakDown(expr, idxFinder, placeHolder=0):
  allSubExprs = {}
  while True:
    idxs = idxFinder(expr)
    if not idxs: return expr, allSubExprs
    if idxs[0][1]-idxs[0][0] == len(expr): return expr, allSubExprs
    expr, subExprs = breakDownExpr(expr, idxs, placeHolder)
    allSubExprs = mergeDict(allSubExprs, subExprs)
    placeHolder+=len(subExprs.keys())

def tokenize(expr, placeHolder=0):
  functionDict={}

  expr, tokens = iterativeBreakDown(expr, findInnerParenthesisRE)
  for k in tokens:
    tokens[k] = tokens[k][1:-1]

  for idxFinder in [findPowRootRE, findMultDivRE, findAddSubRE]:
    expr, newTokens = iterativeBreakDown(expr, idxFinder, placeHolder+len(tokens.keys()))
    tokens = mergeDict(tokens, newTokens)
  return expr, tokens

"""
This class allows a TE to have children that are not directly referenced in expr
Exe:
        10+_2_, {_0_, _1_, _2_}
                  /    |    \
                10*3  2+2  _0_|_1_


class TokenizedExpression:
  def __init__(self, expr, placeHolder=0):
    self.expr, tokens = tokenize(expr,placeHolder)
    self.tokens = {}
    for k in tokens.keys():
      self.tokens[k] = TokenizedExpression(tokens[k], placeHolder+100)#len(self.tokens))

  def __str__(self):
    s=self.expr
    for _ in range(10):
      for k in self.tokens:
        s=s.replace(k, '('+str(self.tokens[k])+')')
    return s

  def showTree(self, indent=""):
    print(indent+"I am ", self.expr)
    print(indent+f"I have {len(self.tokens.keys())} children.")
    for k in self.tokens:
      print(indent+" "+k)
      self.tokens[k].showTree(indent=indent+"   ")
"""

"""
Tree representation of a tokenized expression
Exe:
            10+_2_
               /
            _0_|_1_
            /     \
          10*3    2+2

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
  try: return float(s)
  except: return False

def isPlaceHolder(s):
  return len(s)>2 and s[0]==s[-1]=='_' and all(c.isdigit() for c in s[1:-1])

def isVariable(s): # not a number, not a placeholder, not an operation
  b = not (isNumber(s) or isPlaceHolder(s) or any(c in s for c in OPERANDS))
  return b

def isUnit(s):
  return isNumber(s) or isVariable(s)

def parseUnit(element):
  if isNumber(element):
    return float(element)
  elif isVariable(element):
    return f.Variable(name=element)

isSum = lambda s: '+' in s
isSub = lambda s: '-' in s
isMult = lambda s: '*' in s
isDiv = lambda s: '/' in s
isPow = lambda s: '^' in s
isRoot = lambda s: '|' in s

def treeToFunction(tree):
  #if isUnit(tree.expr): return parseUnit(tree.expr)
  if isNumber(tree.expr):
    return f.Identity(float(tree.expr))
  elif isVariable(tree.expr):
    return f.Identity(f.Variable(name=tree.expr))

  elif isPlaceHolder(tree.expr): return treeToFunction(tree.tokens[tree.expr])

  if isSum(tree.expr):
    symbol='+'
    funct = f.Addition
  elif isSub(tree.expr):
    symbol='-'
    funct = f.Subtraction
  elif isMult(tree.expr):
    symbol='*'
    funct = f.Multiplication
  elif isDiv(tree.expr):
    symbol='/'
    funct = f.Division
  elif isPow(tree.expr):
    symbol='^'
    funct = f.Power
  elif isRoot(tree.expr):
    symbol='|'
    funct = f.Root
  operands=tree.expr.split(symbol)
  operands=[parseUnit(o) if isUnit(o) else treeToFunction(tree.tokens[o]) for o in operands]
  return funct(*operands)

def getFunction(expr):
  return treeToFunction(ExpressionTree(expr))

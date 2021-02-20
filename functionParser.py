import re

import function as F
from utils import mergeDict, decompose
from constants import CONSTANTS

"""
1)
  Code:
    method: utils/decomposeString()
    method: utils/decompose()
    method: tokenize()
    class:  ExpressionTree()

  Parse the function string into a tree representation
  1.1) Split the srting into smaller substrings that reference one another
      Example: function="(2+3)*4" -> function="_0_*4", _0_="2+3"
      We refer to this process as 'tokenization', where:
        - Each substring is called a token
        - The reference to a substring in a sting is called a placeholder
      In the example,
        function="_0_*4" -> the "_0_" in the string is a placeholder
        _0_="2+3" is a token.
      The order followed during tokenization is the same as regular mathemaical
      conventions on the order of operations when evaluating an expression.
      Namely:
        1 - parenthesis
        2 - function-notation operations ( e.g. add(2,3) instead of 2+3 )
        3 - power, root
        4 - multiplication, division
        5 - addition, subtraction
        * - in cases of ambiguity, operations are performed left to right
      For instance:
        start:  expr= "1+(2+3)*4-pw(2,3)"
        step 1: expr=   "1+_0_*4-pw(2,3)", _0_="2+3"
        step 2: expr=       "1+_0_*4-_1_", _0_="2+3", _1_="pw(2,3)"
        step 3: expr=         "1+_2_-_1_", _0_="2+3", _1_="pw(2,3)", _2_="_0_*4"
        step 4: expr=           "_3_-_1_", _0_="2+3", _1_="pw(2,3)", _2_="_0_*4", _3_="1+_2_"

      The function is tokenized, then each token that is created this way is
      itself tokenized, and so on until the main function is split into atomic
      functions. Atomic functions are those that only feature one operation
      (e.g. "2+3", "_0_*4", ...).

  1.2) The tokens are organized into a tree structure, where each node is a
  token having as children the tokens that are referenced by its placeholders.

  Complete example of step 1):
    2+(1+3*4)^(3+1)
    -> Tokenization (1.1)
      Main function is tokenized:
        expr= 2+(1+3*4)^(3+1)
        expr=       2+_0_^_1_, _0_=1+3*4, _1_=3+1
        expr=           2+_2_, _0_=1+3*4, _1_=3+1, _2_=_0_^_1_
      Non-atomic tokens are tokenized:
        _0_= 1+3*4
        _0_= 1+_3_, _3_=3*4
    -> Tree representation (1.2)
          2+_2_
             /
          _0_^_1_
           /    \
         _3_+1  3+1
          /
         3*4
  Note:
    In the actual implementation, steps 1.1 and 1.2 are not so well distinct.
    In particular, a simplified algorithm that illustrates how the tree is
    actually built is:
      class Tree
        List<Tree> children
        method initialization(funStr)
          tokens = tokenize(funStr)
          if (tokens.lenght!=0)
            for (token in tokens)
              children.add( Tree(token) )
    - tokenize the function and organize it into a first tree
    - tokenize each obtained token and organize it into a second tree,
      with the first tree having a reference to the second one; and so on

2)
  Code:
    class:  Function/BinaryFunction() and subclasses
    method: treeToFunction()

  Convert the tree representation into a Function object.
  Starting from the root of the tree, recursively.
  First, the operation and the arguments are identified.
  To each operation corresponds a BinaryFunction subclass.
  For each argument:
    if it can be casted into a float, it is
    if it is a variable, it is converted into a Variable object
    if it is a placeHolder, the corresponding token in parsed (recursive call)
  The BinaryFunction object is returned with the arguments
  Examples:
    1+2 -> Addition(1,2)
    1+x -> Addition(1, Variable('x'))
    3*_0_
       /   -> Multiplication(3, Addition(2,4))
      2+4
  Flow example:
    3*_0_
       /
      2+4
  '3*_0_' ->    Op: '*'   -> Multiplication
             Arg 1: '3'   -> 3.0
             Arg 2: '_0_' -> '2+4' => ---------------Recursive-call----------------  => Multiplication(3, Addition(2,4))
                                      |    Op: '+' -> Addition                    |
                                      | Arg 1: '2' -> 2.0        -> Addition(2,4) |
                                      | Arg 1: '4' -> 4.0                         |
                                      ---------------------------------------------

"""

PATTERN_PAR = '\([^\(\)]*\)' # 2+2+12*(1*(2/3)+2)+11 -> (2/3)
PATTERN_PH = '_[0-9]+_'

OPERANDS = list("+-*/^|!") # TODO reaname OPERATIONS
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

def findFractalRE(expr):
  pattern = '[^\+\-\*\/]+!'
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
  for idxFinder in [findKeyWordsRE, findKeyWordsArgsRE, findFractalRE, findPowRootRE, findMultDivRE, findAddSubRE]:
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
isFractal     = lambda s: '!' == s[-1]
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
  # this is only true if the starting expression is a single number or variable
  if isUnit(tree.expr): return F.Identity(parseUnit(tree.expr))

  if isPlaceHolder(tree.expr): return treeToFunction(tree.tokens[tree.expr])

  if isKeyWord(tree.expr):
    fun = tree.expr[:2]
    operands=[parseUnit(o) if isUnit(o) else treeToFunction(tree.tokens[o]) for o in tree.expr[3:-1].split(',')]
    if   fun=='lg': return F.Logarithm(*operands)
    elif fun=='pw': return F.Power(*operands)
    elif fun=='rt': return F.Root(*operands)

  if isSum(tree.expr):
    arguments = tree.expr.split('+')
    funct = F.Addition
  elif isSub(tree.expr):
    arguments = tree.expr.split('-')
    funct = F.Subtraction
  elif isMult(tree.expr):
    arguments = tree.expr.split('*')
    funct = F.Multiplication
  elif isDiv(tree.expr):
    arguments = tree.expr.split('/')
    funct = F.Division
  elif isPow(tree.expr):
    arguments = tree.expr.split('^')
    funct = F.Power
  elif isRoot(tree.expr):
    arguments = tree.expr.split('|')
    funct = F.Root
  elif isFractal(tree.expr):
    arguments = [tree.expr[:-1]]
    funct = F.Fractal
  else: return # TODO error
  operands=[parseUnit(a) if isUnit(a) else treeToFunction(tree.tokens[a]) for a in arguments]
  return funct(*operands)

def replaceConstants(expr):
  for c in CONSTANTS:
    expr=expr.replace(c.name, str(c.value))
  return expr

def preprocess(expr):
  expr=expr.replace(' ','')
  if expr[0]=='-': expr='0'+expr
  expr=replaceConstants(expr)
  return expr

def getFunction(expr):
  expr = preprocess(expr)
  return treeToFunction(ExpressionTree(expr))

import re

OPERATIONS = list("+-*/^|!")
KEYWORDS = ['rt', 'pw', 'lg']

def getBasicPattern(ops, pairOnly=False, left=True, right=True):
  excludedStr = '\\'+'\\'.join(o for o in OPERATIONS if (o not in ops or pairOnly))
  selectedStr = '\\'+'\\'.join(o for o in ops)
  pattern = f"[{selectedStr}]"
  if left: pattern = f"[^{excludedStr}]+"+pattern
  if right: pattern = pattern+f"[^{excludedStr}]+"
  return pattern

class SubstringFinder:
  def find(self, s):
    pass

class SubstringFinderRE(SubstringFinder):
  def __init__(self, pattern):
    super(SubstringFinderRE, self).__init__()
    self.pattern=pattern
  def find(self, s):
    return [(m.start(0), m.end(0)) for m in re.finditer(self.pattern, s)]

class AddSubFinder(SubstringFinderRE):
  def __init__(self):
    pattern = getBasicPattern(["+","-"], pairOnly=True)
    super(AddSubFinder, self).__init__(pattern)

class MultDivFinder(SubstringFinderRE):
  def __init__(self):
    pattern = getBasicPattern(["*","/"], pairOnly=True)
    super(MultDivFinder, self).__init__(pattern)

class PowRootFinder(SubstringFinderRE):
  def __init__(self):
    pattern = getBasicPattern(["^","|"], pairOnly=True)
    super(PowRootFinder, self).__init__(pattern)

class FactorialFinder(SubstringFinderRE):
  def __init__(self):
    pattern = getBasicPattern(["!"], pairOnly=True, left=True, right=False)
    super(FactorialFinder, self).__init__(pattern)

class KeyWordFinder(SubstringFinderRE):
  def __init__(self, keyword):
    pattern = keyword+'\([^\(\)]*\)'
    super(KeyWordFinder, self).__init__(pattern)

class KeyWordsFinder(SubstringFinder):
  def find(self, s):
    idxs=[]
    for keyword in KEYWORDS:
      idxs += KeyWordFinder(keyword).find(s)
    return idxs

class KeyWordsArgsFinder(SubstringFinder):
  def find(self, s):
    pattern = "\(.*["+'\\'+'\\'.join(OPERATIONS)+"].*\,"  # NOTE "\(.*\," would yeld infinite loop
    idxs = [(m.start(0)+1, m.end(0)-1) for m in re.finditer(pattern, s)]
    pattern = "\,.*["+'\\'+'\\'.join(OPERATIONS)+"].*\)"
    idxs= idxs+[(m.start(0)+1, m.end(0)-1) for m in re.finditer(pattern, s)]
    return idxs

class InnerParenthesisFinder(SubstringFinder):
  def find(self, s):
    # find parenthesis that have no inner parenthesis, except for function notation
    """
    Complete exmaple:
      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=-1, toSkip=0, idxs=[]
      |

      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=2, toSkip=0, idxs=[]
        |
      
      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=5, toSkip=0, idxs=[]
           |

      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=-1, toSkip=0, idxs=[(5,10)]
               |

      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=11, toSkip=0, idxs=[(5,10)]
                 |

      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=11, toSkip=1, idxs=[(5,10)]
                    |
      
      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=11, toSkip=0, idxs=[(5,10)]
                         |
      
      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=-1, toSkip=0, idxs=[(5,10), (11,24)]
                             |
      
      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=25, toSkip=0, idxs=[(5,10), (11,24)]
                               |
      
      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=25, toSkip=1, idxs=[(5,10), (11,24)]
                                    |
      
      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=33, toSkip=0, idxs=[(5,10), (11,24)]
                                       |

      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=-1, toSkip=0, idxs=[(5,10), (11,24), (33,38)]
                                           |

      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=-1, toSkip=0, idxs=[(5,10), (11,24), (33,38)]
                                            |
      
      1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1)))) => openIdx=-1, toSkip=0, idxs=[(5,10), (11,24), (33,38)]
                                              |
    """

    idxs = []
    openIdx=-1 # index of last open parenthesis met, function-notation excluded
    toSkip=0 # nr of function-notation open parenthesis met not yet closed, since openIdx (since last open parenthesis excluded function-notation)
    for i,c in enumerate(s):
      if c == '(':
        if s[i-2:i] in KEYWORDS: toSkip+=1
        else:
          openIdx=i
          toSkip=0
      elif c == ')' and openIdx!=-1:
        if toSkip!=0:
          toSkip-=1
          continue
        idxs.append((openIdx, i+1))
        openIdx=-1
    return idxs


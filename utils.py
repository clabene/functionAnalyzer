def mergeDict(d1, d2):
  return dict(d1, **d2)

"""
ciao come va, [(5,9)]              ->  ciao _0_ va, {_0_:come}
(2+3)+(5+6)+1, [(0,5), (6,10)]     ->  _0_+_1_+1, {_0_:(2+3), _1_:(5+6)}
(2+3)+(5+6)+1, [(0,5), (6,10)], 10 ->  _10_+_11_+1, _10_:(2+3), _11_:(5+6)
"""
def decomposeString(expr, idxs, placeHolder=0):
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
def decompose(expr, idxFinder, placeHolder=0):
  allSubExprs = {}
  while True:
    idxs = idxFinder(expr)
    if not idxs: return expr, allSubExprs
    if idxs[0][1]-idxs[0][0] == len(expr): return expr, allSubExprs
    expr, subExprs = decomposeString(expr, idxs, placeHolder)
    allSubExprs = mergeDict(allSubExprs, subExprs)
    placeHolder+=len(subExprs.keys())

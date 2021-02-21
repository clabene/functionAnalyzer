import substringFinder as ssf

def test(expected, finder, s, **kwargs):
  idxs = finder(**kwargs).find(s)
  found = [s[l:r] for l,r in idxs]
  assert expected == found, f"Expected: {expected}, but got: {found}. s={s}"

ds = [
  {"expected":["3+2"], "finder":ssf.AddSubFinder, "s":"3+2*1"},

  {"expected":["(3+2)"], "finder":ssf.ParenthesisFinder, "s":"(3+2)*1"},
  {"expected":["(3+2+pw(2,3))"], "finder":ssf.ParenthesisFinder, "s":"2+(3+2+pw(2,3))*1"},
  {"expected":[], "finder":ssf.ParenthesisFinder, "s":"3+2*1"},
  {"expected":["(lg(2,3))"], "finder":ssf.ParenthesisFinder, "s":"(lg(2,3))"},
  {"expected":["(lg(2,3))"], "finder":ssf.ParenthesisFinder, "s":"2+pw(3,2)+2*(lg(2,3))"},
  {"expected":["(2+pw(3,2)+2*lg(2,3))"], "finder":ssf.ParenthesisFinder, "s":"(2+pw(3,2)+2*lg(2,3))"},
  {"expected":["(3)", "(2*rt(1,1))"], "finder":ssf.ParenthesisFinder, "s":"((3)*4 +(2*rt(1,1)))"},
  {"expected":["(3*2)", "(pw(2+3,4)*2)", "(3+1)"], "finder":ssf.ParenthesisFinder,
    "s":"1+(1+(3*2)+(pw(2+3,4)*2)+(1+lg(2,(3+1))))"},
  
  {"expected":["pw(3+2,3)"], "finder":ssf.KeyWordsFinder, "s":"pw(3+2,3)*1"},
  {"expected":["lg(3,5)"], "finder":ssf.KeyWordsFinder, "s":"pw(3+2,lg(3,5))*1"},
  {"expected":["pw(3+2,0)","lg(3,5)"], "finder":ssf.KeyWordsFinder, "s":"pw(pw(3+2,0),lg(3,5))"},

  {"expected":["3+2","4*2"], "finder":ssf.KeyWordsArgsFinder, "s":"pw(3+2,4*2)"},
]

for d in ds: test(**d)
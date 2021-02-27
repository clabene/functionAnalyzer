from substringFinderTest import SubstringFinderTest
from functionParserTest import FunctionParserTest
from monteCarloTest import MonteCarloWithIntegralTest, MonteCarloWithSolutionTest
from optimizeTest import OptimizeTest

def runTest(T):
  for data in T.generateData():
    T.test(**data)

# runTest(SubstringFinderTest())
# runTest(FunctionParserTest())
# runTest(MonteCarloWithIntegralTest())
# runTest(MonteCarloWithSolutionTest())
runTest(OptimizeTest())
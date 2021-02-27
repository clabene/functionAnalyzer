from substringFinderTest import SubstringFinderTest
from functionParserTest import FunctionParserTest
from monteCarloTest import MonteCarloWithIntegralTest, MonteCarloWithSolutionTest
from optimizeTest import OptimizeTest
from derivativeTest import FullDerivativeTest, EqualityDerivativeTest

def runTest(T):
  for data in T.generateData():
    T.test(**data)

# runTest(SubstringFinderTest())
# runTest(FunctionParserTest())
# runTest(MonteCarloWithIntegralTest())
# runTest(MonteCarloWithSolutionTest())
runTest(OptimizeTest())
runTest(FullDerivativeTest())
runTest(EqualityDerivativeTest())

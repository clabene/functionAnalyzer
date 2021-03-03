from Tests.substringFinderTest import SubstringFinderTest
from Tests.functionParserTest import FunctionParserTest
from Tests.monteCarloTest import MonteCarloWithIntegralTest, MonteCarloWithSolutionTest
from Tests.optimizeTest import OptimizeTest
from Tests.derivativeTest import FullDerivativeTest, EqualityDerivativeTest

def runTest(T):
  for data in T.generateData():
    T.test(**data)

runTest(SubstringFinderTest())
runTest(FunctionParserTest())
runTest(MonteCarloWithIntegralTest())
runTest(MonteCarloWithSolutionTest())
runTest(OptimizeTest())
runTest(FullDerivativeTest())
runTest(EqualityDerivativeTest())

import unittest
import codeBlockHelperTests
import BlockTestCases
import BlockLocatorTestCases
import sys

if __name__ == '__main__':
    loader = unittest.TestLoader()
    ltm = loader.loadTestsFromModule
    runner = unittest.TextTestRunner(stream = sys.stdout, descriptions=2, verbosity=2)
    all = unittest.TestSuite([
        ltm(BlockTestCases), 
        ltm(codeBlockHelperTests), 
        ltm(BlockLocatorTestCases),
        ])
    runner.run(all)

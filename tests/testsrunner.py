import unittest
import codeBlockHelperTests
import BlockTestCases
import BlockLocatorTestCases
import packagerTestCases
import sys

if __name__ == '__main__':
    loader = unittest.TestLoader()
    ltm = loader.loadTestsFromModule
    runner = unittest.TextTestRunner(stream = sys.stdout, descriptions=3, verbosity=3)
    all = unittest.TestSuite([
        ltm(BlockTestCases), 
        ltm(codeBlockHelperTests), 
        ltm(BlockLocatorTestCases),
        ltm(packagerTestCases)
        ])
    runner.run(all)

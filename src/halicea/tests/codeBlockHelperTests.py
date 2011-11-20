import unittest
import os
from os.path import join as pjoin
import shutil
resDir = os.path.join(os.path.dirname(__file__), 'resources')
from halicea.lib.codeBlocksHelpers import  strBetween 

class CodeBlockHelperTests(unittest.TestCase):
    def setUp(self):
        self.fileName = pjoin(resDir, 'testBlockTree.html')
        self.tmpPath = pjoin(resDir, 'testBlocks.testres')
        shutil.copy(self.fileName, self.tmpPath)
        self.blockDict = {'grandchild':['__Line4__'],}
        self.blockDictExistingTest = {'grandchild':['      Line3'],}

    def test_strBetween(self):
        testDict = {'blab Result lab':['blab', 'lab', False, ' Result '], 
                    'adrgbwsrthbftr blab Result asdtrh labaergaerg':[ 'blab', 'lab', False, ' Result asdtrh '],
                    'blab Result lab':['blab', 'lab', True, 'Result'],
                    'adrgbwsrthbftr blab Result asdtrh labaergaerg':['blab', 'lab', True, 'Result asdtrh']
                    }
        for k in testDict.keys():
            self.assertEquals(strBetween(k, testDict[k][0], testDict[k][1], testDict[k][2]), testDict[k][3])
    def tearDown(self):
        os.remove(self.tmpPath)

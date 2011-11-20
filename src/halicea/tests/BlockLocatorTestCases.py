import unittest
from halicea.lib.codeBlocksHelpers import *

class BlockLocatorTestCase(unittest.TestCase):
    def setUp(self):
        self.blockContent="""first
second
thirt
fourth
fifth"""
        self.getTmpl = """$blindent## $blockname ##
#content#
$blindent## end_$blockname ##
"""
        def beginMatch(line):
            if line.strip().startswith('## ') and line.strip().endswith(' ##'):
                return line.strip()[3:-2].strip()
            else:
                return None
        def endMatch(line):
            return line.strip().startswith('## end') and line.strip().endswith(' ##')
        self.locatorHal = HalCodeBlockLocator()
        self.locatorGen = GenericCbl(beginMatch, endMatch, self.getTmpl)
    
    def test_HalLocator(self):
        result =self.locatorHal.createValidBlock('test', self.blockContent.split('\n'), blIndent=0, indent=4)
        expected= """{%block test%}
    first
    second
    thirt
    fourth
    fifth
{%endblock%}
"""
        self.assertEquals(result, expected)
    
    def test_GenLocator(self):
        result =self.locatorGen.createValidBlock('test', self.blockContent.split('\n'), blIndent=0, indent=4)
        expected= """## test ##
    first
    second
    thirt
    fourth
    fifth
## end_test ##
"""
        self.assertEquals(result, expected)
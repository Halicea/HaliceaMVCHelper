#!/usr/bin/env python
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
from string import Template

class BlockLocator(object):
    blockTemplate = None
    def lineIsBlockBegin(self):
        pass
    def lineIsBlockEnd(self):
        pass
    def createValidBlock(self, blockname, content=[], blIndent=0, indent=0):
        if not self.blockTemplate:
            raise NotImplementedError('Block Template was not provided')
        result = Template(self.blockTemplate).substitute(blindent=' '*blIndent, blockname=blockname)
        if not content:
            return result.replace('#content#\n','')
        else:
            return result.replace('#content#','\n'.join([(' '*indent)+line for line in content]))

class GenericCbl(BlockLocator):
    """base class for all BlockLocators"""
    def __init__(self, blockBeginLocator, blockEndLocator, blockTemplate=None):
        self.blockTemplate = blockTemplate
        self.lineIsBlockBegin = blockBeginLocator
        self.lineIsBlockEnd = blockEndLocator

class HalCodeBlockLocator(BlockLocator):
    blockTemplate = '''$blindent{%block $blockname%}
#content#
$blindent{%endblock%}
'''
    def lineIsBlockBegin(self, line):
        if line.replace(' ','').find('{%block')>=0 and line.replace(' ','').find('%}')>0:
            return strBetween(line.replace(' ',''), '{%block', '%}')
        else: 
            return None
    def lineIsBlockEnd(self, line):
        return line.replace(' ','').find('{%endblock%}')>=0

class InPythonBlockLocator(BlockLocator):
    blockTemplate = \
'''$blindent#{%block $blockname%}
#content#
$blindent#{%endblock%}
'''
    def lineIsBlockBegin(self, line):
        if line.replace(' ','').find('#{%block')>=0 and line.replace(' ','').find('%}')>0:
            return strBetween(line.replace(' ',''), '#{%block', '%}')
        else: 
            return None
    def lineIsBlockEnd(self, line):
        return line.replace(' ','').find('#{%endblock%}')>=0

def strBetween(line, strLeft, strRigth, strip=True ):
    fromIndex=line.index(strLeft)+len(strLeft)
    toIndex = fromIndex+line[fromIndex:].index(strRigth)
    result = line[fromIndex:toIndex]
    if strip: 
        return result.strip()
    else: 
        return result

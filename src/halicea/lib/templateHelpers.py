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
from config import djangoVars
def convertToTemplate(text,input={}):
    result = text
    for k, v in djangoVars.iteritems():
        result=result.replace(v,'{-{'+k+'}-}')
    for k, v in input.iteritems():
        result=result.replace(v,'{-{'+k+'}-}')
    result = result.replace('{-{','{{')
    result = result.replace('}-}','}}')
    return result

def convertToReal(text,input={}):
    result = text
    for k, v in djangoVars.iteritems():
        result=result.replace(k, v)
    for k, v in input.iteritems():
        result=result.replace(k, v)
    return result

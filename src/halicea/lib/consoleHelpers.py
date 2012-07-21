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
def extractAgrs(paramsList):
    return dict(map(lambda x:(x[:x.index('=')], x[x.index('=')+1:]), paramsList))

def ask(message, validOptions={'y':True,'n':False}, input=raw_input):
    yesno =''
    if isinstance(validOptions, str):
        #print validOptions
        yesno = input(message)
    else:
        #print validOptions.keys()
        yesno = input(message+'('+'/'.join(validOptions.keys())+'):')
    while True:
        if validOptions=='*':
            return yesno
        if len(yesno)>0: 
            if validOptions.has_key(yesno):
                return validOptions[yesno]
        print 'Not Valid Input'
        yesno = input(message+'('+'/'.join(validOptions.keys())+'):')

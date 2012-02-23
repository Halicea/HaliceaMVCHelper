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
#along with this program.  If not, see <http://www.gnu.org/licenses/>.import os
if os.name!='nt':
    import readline
#AutoCompletion
values =['project', 'mvc','vc','mc', 'mv','m','v','c','run','deploy']
modelsStructure ={}
commandsDict={'*':{ 'new':{'template':{}, 'real':{}}, 'project':{},
                    'mvcfh':{},
                    'del':{'package':{}, 'model':{}},
                    'deploy':{'--no_cookies':{},'--email=':{}},
                    'run':{'--port=':{}, '--clear_datastore=':{}, '--datastore_path=':{}},
                    'pack':{'package':{}},
                    'unpack':{'package':{}},
                    'git':{'status':{}, 'log':{},'init':{}, 'push':{'origin':{'master':{}}}, 'commit':{'-a':{}, '-am \"':{}}, 'add':{'.':{}} },
                    'deploy':{},
                    'exit':{},
                    }
                }
mvcStates = {'package':{},'class':{}, 'prop':{'ref':modelsStructure} }
completions={}
currentState = ''
def completer(text, state):
    line = readline.get_line_buffer()
    enterstate = line.split()
    enterstate.insert(0,'*')
    if line and not line[-1]==' ':
        searchText = enterstate.pop()
    else:
        searchText = ''
    finalDict = commandsDict
    try:
        for k in enterstate:
            finalDict = finalDict[k]
    except:
        finalDict = {}
    matches = [value for value in finalDict.iterkeys() if value.upper().startswith(searchText.upper())]
    try:
        return matches[state]
    except IndexError:
        return None

def set_completer():
    if os.name!='nt':
        readline.set_completer(completer)
        readline.parse_and_bind('tab: menu-complete')
    baseusage = """
Usage haliceamvc.py [projectPath]
Options: [create]
"""
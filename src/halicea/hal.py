#!/usr/bin/env python
import sys, subprocess, webbrowser, os
from os.path import join as pjoin
from string import Template
#-----------------

from halicea.lib.config import INSTALL_LOC, PROJ_LOC
from halicea.lib.consoleHelpers import extractAgrs
from halicea.lib.ioUtils import saveTextToFile, getTextFromPath
from halicea.lib.mvcManager import makeMvc, delMvc
from halicea.lib.projectManager import newProject
from halicea.lib.codeBlocksHelpers import HalCodeBlockLocator, InPythonBlockLocator
from halicea.lib.templateHelpers import convertToReal, convertToTemplate
from halicea.lib import config
from halicea.lib.packager import Packager
cblPy = InPythonBlockLocator()
cblHal = HalCodeBlockLocator()
if os.name!='nt':
    import readline

def tail(arr, cnt):
    if len(arr)<cnt:
        return []
    else:
        return arr[-cnt:]
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

if os.name!='nt':
    readline.set_completer(completer)
    readline.parse_and_bind('tab: menu-complete')
baseusage = """
Usage haliceamvc.py [projectPath]
Options: [create]
"""

isInInstall = True #os.path.exists(pjoin(INSTALL)LOC, '.InRoot'))
def main(args):
    packager = Packager(raw_input)
    # can do this in install on local mode
    if args[0]=='new' and len(args)>2:
        if args[1]=='template':
            templ = getTextFromPath(args[2])
            input=len(args)>3 and extractAgrs(args[3:]) or {}
            txt = convertToTemplate(templ, input)
            print txt; print
            saveTextToFile(txt)
            return
        elif args[1] =='real':
            templ = getTextFromPath(args[2])
            input=len(args)>3 and extractAgrs(args[3:]) or {}
            txt = convertToReal(templ, input)
            print txt; print
            saveTextToFile(txt)
            return
        elif not isInInstall:
            print 'Not valid type for new'
            return
#    isInInstall=True
    if isInInstall:
        #print args
        if args[0]=='project' and len(args)>1:
            newProject(args[1])
#        else:
#            print 'Not a valid command'
#        return
    if True:
        if set(args[0]).issubset(set('mvfch')):
            makeMvc(args)
        elif args[0]=='del' and len(args)>=2:
            if args[1]=='package':
                pname = ''
                if len(args)==2:
                    pname = raw_input('Enter Package Name: ')
                else:
                    pname=args[2]
                packager.delete(pname)
            elif set(args[1]).issubset(set('mvc')):
                cname = ''
                pname = ''
                if len(args)==2:
                    cname=raw_input('EnterTheModelClass: ')
                else:
                    cname=args[2]
                delMvc(args[1], cname)
        elif args[0]=='run':
            options = ''
            if len(args)>1:
                options = ' '.join(args[1:])
            command = Template('python $appserver $proj $options').substitute(
                                    appserver = pjoin(config.APPENGINE_PATH, 'dev_appserver.py'),
                                    proj=config.PROJ_LOC,
                                    options = options)
            # print command
            subprocess.Popen(command, shell=True, stdout=sys.stdout, stdin=sys.stdin).wait()
            #webbrowser.open('http://localhost:8080')
        elif args[0]=='pack' and len(args)>3:
            if args[1]=='package':
                packager.pack(args[2], args[3])
        elif args[0]=='unpack' and len(args)>=3:
            if args[1]=='package':
                packager.unpack(args[2], args[3])
        elif args[0]=='deploy':
            options = ''
            if len(args)>1:
                options = ' '.join(args[1:])
            command = Template('python $appcfg update $options $proj').substitute(
                                  appcfg = pjoin(config.APPENGINE_PATH, 'appcfg.py'),
                                  proj = config.PROJ_LOC,
                                  options = options)
            subprocess.Popen(command, shell=True).wait()
        elif args[0]=='console':
            pass
        elif args[0]=='git':
            subprocess.Popen(' '.join(args), shell=True, stdout=sys.stdout, stdin=sys.stdin, stderr=sys.stderr).wait()
        elif args[0]=='clear':
            subprocess.Popen('clear', shell=True, stdout=sys.stdout, stdin=sys.stdin, stderr=sys.stderr).wait()
        else:
            print 'Not Valid Command [mvc, run, console]'
        return
def main_safe(*allargs):
    if os.pathsep in allargs[0]:
        os.chdir(allargs[0])
    try:
        print 'Opening Project', PROJ_LOC
        if len(allargs)>1:
            main(allargs[1:])
        else:
            'Halicea Command Console is Opened'
            while True:
                args =raw_input('hal>').split()
                if not(len(args)==1 and args[0]=='exit'):
                    try:
                        main(args)
                    except Exception,ex:
                        print ex
                        print sys.exc_info()
                else:
                    print 'Halicea Command Console exited'
                    break;
    except KeyboardInterrupt:
        print 'Halicea Command Console exited'
def real_main():
    main_safe(sys.argv)
if __name__ == '__main__':
    real_main()

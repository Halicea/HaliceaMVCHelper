#!/usr/bin/env python
import sys, subprocess, os
from os.path import join as pjoin
from string import Template
from pprint import pprint
#-----------------
import halicea
from halicea.lib.consoleHelpers import extractAgrs
from halicea.lib.ioUtils import saveTextToFile, getTextFromPath
from halicea.lib.mvcManager import MVCManager
from halicea.lib.projectManager import ProjectManager
from halicea.lib.codeBlocksHelpers import HalCodeBlockLocator, InPythonBlockLocator
from halicea.lib.templateHelpers import convertToReal, convertToTemplate
from halicea.lib import config
from halicea.lib.packager import Packager

cblPy = InPythonBlockLocator()
cblHal = HalCodeBlockLocator()
project = halicea.get_current_project()

def tail(arr, cnt):
  if len(arr)<cnt:
    return []
  else:
    return arr[-cnt:]

isInInstall = config.INSTALL_LOC == os.path.dirname(config.PROJ_LOC)
def main(args):
  packager = Packager(raw_input)
  project_manager = ProjectManager(project)
  mvc_manager = MVCManager(project)
  
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
    elif args[1]=='project' and len(args)>2:
      if isInInstall:
        project_manager.newProject(args[2])
      else: 
        print 'Not valid type for new when in project'
      return 
  elif not isInInstall:
    if set(args[0]).issubset(set('mvfc')):
      mvc_manager.makeMvc(args)
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
        mvc_manager.delMvc(args[1], cname)
    elif args[0]=='run':
      options = ''
      if len(args)>1:
        options = ' '.join(args[1:])
      
      command = Template('python $appserver $proj $options').substitute(
                  appserver = pjoin(config.APPENGINE_PATH, 'dev_appserver.py'),
                  proj=config.PROJ_LOC,
                  options = options)
      subprocess.Popen(command, shell=True, stdout=sys.stdout, stdin=sys.stdin).wait()
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
    elif args[0]=='list':
      if len(args)>1 and args[1]=='packages':
        packager.listPackages()
      elif len(args)>1 and args[1]=='details':
        pprint(project)
    else:
      print 'Not Valid Command'
  else:
    print 'Not Valid Command'
  return
def main_safe(*allargs):
  if os.pathsep in allargs[0]:
    os.chdir(allargs[0])
  try:
    print 'Opening Project', project.path
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
  main_safe(*sys.argv)
if __name__ == '__main__':
  real_main()

from config import proj_settings
from os.path import join as pjoin, basename
import os, shutil, pprint
from consoleHelpers import ask
from string import Template
from baseClasses import Block
from locators import *
from codeBlocksHelpers import HalCodeBlockLocator, InPythonBlockLocator
from halicea import dirtree
cblHal = HalCodeBlockLocator()
cblPy = InPythonBlockLocator()
from copy import deepcopy

packageStructure = {
'forms_d':pjoin(proj_settings.FORM_VIEWS_DIR, '${package}'),
'styles_d':pjoin(proj_settings.STYLES_DIR, '${package}'),
'pages_d':pjoin(proj_settings.PAGE_VIEWS_DIR, '${package}'),
'jscripts_d':pjoin(proj_settings.JSCRIPTS_DIR, '${package}'),
'Forms.py_f':pjoin(proj_settings.FORM_MODELS_DIR, '$package'+proj_settings.MODEL_FORM_MODULE_SUFIX+'.py'),
'Models.py_f':pjoin(proj_settings.MODELS_DIR, '${package}' + proj_settings.MODEL_MODULE_SUFIX + '.py'),
'Controllers.py_f':pjoin(proj_settings.CONTROLLERS_DIR, '${package}' + proj_settings.CONTROLLER_MODULE_SUFIX + '.py'),
'url.map':proj_settings.HANDLER_MAP_FILE,
}

def copyItem(src, dest, dType):
    if dType == 'd':
        if os.path.exists(src):
            print 'exporting', src, 'directory to', dest
            shutil.copytree(src, dest)
        else:
            print src, 'does not exists'
    elif dType == 'f':
        if os.path.exists(src):
            print 'exporting', src, 'as', dest
            shutil.copy(src, dest)
        else:
            print src, 'does not exists'

def __pack__(packageName, destination):
    for key in packageStructure.keys():
        if key.find('_')>0:
            (destName, dType) = key.split('_')
            dest = pjoin(destination, destName)
            src = Template(packageStructure[key]).substitute(package=packageName)
            copyItem(src, dest, dType)
    handlerMap = Block.loadFromFile(proj_settings.HANDLER_MAP_FILE, cblPy)
    map = handlerMap['ApplicationControllers'][packageName+proj_settings.CONTROLLER_MODULE_SUFIX]
    imports  = handlerMap['imports']
def __unpack__(packageName, source):
    for key in packageStructure.keys():
        if key.find('_')>0:
            (srcName, dType) = key.split('_')
            src = pjoin(source, srcName)
            dest = Template(packageStructure[key]).substitute(package=packageName) 
            copyItem(src, dest, dType)

def pack(packageName, destination):
    if os.path.exists(destination):
        if os.path.isdir(destination):
            if ask('Directory Already Exists, All contents will be deleted, Do you want to continue?'):
                shutil.rmtree(destination)
                os.makedirs(destination)
                __pack__(packageName, destination)
            else:
                return
        else:
            print 'There is file with the same name, Cannot continue!'
            return
    else:
        __pack__(packageName, destination)
def unpack(packageName, source):
    if os.path.exists(source):
        __unpack__(packageName, source)
    else:
        print 'Such Package does not exist'
def delete(pname):
    pmfile = LocateModelModule(pname)
    pcfile = LocateControllerModule(pname)
    pfmfile = LocateFormModelModule(pname)
    
    pmdir = BasePathFromName(pname)
    pcdir = BasePathFromName(pname)
    pfmdir = BasePathFromName(pname)
    
    pvdir = LocatePagesDir(pname)
    pfdir =LocateFormsDir(pname)
    handlermapblock1 = pname+settings.CONTROLLER_MODULE_SUFIX
    handlermapblock2 = pname
    handlermapimport = 'from '+basename(settings.CONTROLLERS_DIR)+' import '+pname+settings.CONTROLLER_MODULE_SUFIX

    print 'This paths will be permanently deleted'
    for item in [pmfile, pfmfile, pcfile, pmdir,pcdir, pfmdir,pvdir, pfdir]:
        if os.path.exists(item):
            if os.path.isdir(item):
                print item
                dirtree.tree(item, ' ', print_files=True, depth=3)
            else:
                print item
    if ask('Are you sure you want to delete the Package %s?'%pname):
        for item in [pmfile, pfmfile, pcfile, pmdir,pcdir, pfmdir,pvdir, pfdir]:
            if os.path.exists(item):
                if os.path.isdir(item):
                    print 'removing %s directory'%item
                    shutil.rmtree(item)
                else:
                    print 'removing %s file'%item
                    os.remove(item)
            else:
                print 'Path %s does not exist'%item
        handlerMap = Block.loadFromFile(settings.HANDLER_MAP_FILE, cblPy)
        impLine = handlerMap['imports'][handlermapimport]
        #remove the import
        if impLine:
            handlerMap['imports'].remove(impLine)
        else:
            print 'import \'', handlermapimport, '\'does not exists'
        #Remove the urlMap Block
        mapBl = handlerMap['ApplicationControllers'][handlermapblock2]
        if mapBl:
            print 'removing block:'
            print str(mapBl)
            handlerMap['ApplicationControllers'].remove(mapBl)
        mapBl = handlerMap['ApplicationControllers'][handlermapblock1]
        if mapBl:
            print 'removing block:'
            print str(mapBl) 
            handlerMap['ApplicationControllers'].remove(mapBl)
        handlerMap.saveToFile(settings.HANDLER_MAP_FILE)
        print 'Package %s was removed'%pname
    else:
        pass

from config import proj_settings
from os.path import join as pjoin
import os, shutil
from consoleHelpers import ask
from string import Template
from baseClasses import Block
from codeBlocksHelpers import HalCodeBlockLocator, InPythonBlockLocator
cblHal = HalCodeBlockLocator()
cblPy = InPythonBlockLocator()
from copy import deepcopy

packageStructure = {
'forms_d':pjoin(proj_settings.FORM_VIEWS_DIR, '${package}'),
'styles_d':pjoin(proj_settings.STYLES_DIR, '${package}'),
'pages_d':pjoin(proj_settings.PAGE_VIEWS_DIR, '${package}'),
'jscripts_d':pjoin(proj_settings.JSCRIPTS_DIR, '${package}'),
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
        if key.index('_'):
            (destName, dType) = key.split('_')
            dest = pjoin(destination, destName)
            src = Template(packageStructure[key]).substitute(package=packageName)
            copyItem(src, dest, dType)
    handlerMap = Block.loadFromFile(proj_settings.HANDLER_MAP_FILE, cblPy)
    map = handlerMap['ApplicationControllers'][packageName+proj_settings.CONTROLLER_MODULE_SUFIX]
    imports  = handlerMap['imports']
def __unpack__(packageName, source):
    for key in packageStructure.keys():
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

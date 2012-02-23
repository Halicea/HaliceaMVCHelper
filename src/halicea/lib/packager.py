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
#along with this program.  If not, see <http://www.gnu.org/licenses/>.from os.path import join as pjoin, basename
import os, shutil, pprint
from consoleHelpers import ask
from string import Template
from baseClasses import Block
from locators import *
from codeBlocksHelpers import HalCodeBlockLocator, InPythonBlockLocator
import dirtree
from halicea.lib.baseClasses import Block
from halicea.lib import projectManager
cblHal = HalCodeBlockLocator()
cblPy = InPythonBlockLocator()
from copy import deepcopy
from config import proj_settings
import config

def restrictBaseProjectAccess(func):
    def ret(*args, **kwargs):
        if os.path.dirname(config.PROJ_LOC) == config.INSTALL_LOC:
            raise Exception('Not allowed to run this operation against Hal')
        return func(*args, **kwargs)
    return ret
class Packager(object):
    def __init__(self, input_method):
        self.input_method= input_method
        self.packageStructure = {
        'forms_d':pjoin(proj_settings.FORM_VIEWS_DIR, '${package}'),
        'styles_d':pjoin(proj_settings.STYLES_DIR, '${package}'),
        'pages_d':pjoin(proj_settings.PAGE_VIEWS_DIR, '${package}'),
        'jscripts_d':pjoin(proj_settings.JSCRIPTS_DIR, '${package}'),
        'models_d':pjoin(proj_settings.MODELS_DIR, '${package}'),
        'controllers_d':pjoin(proj_settings.CONTROLLERS_DIR, '${package}'),
        'formmodels_d':pjoin(proj_settings.FORM_MODELS_DIR, '${package}'),
        'Forms.py_f':pjoin(proj_settings.FORM_MODELS_DIR, '${package}'+proj_settings.MODEL_FORM_MODULE_SUFIX+'.py'),
        'Models.py_f':pjoin(proj_settings.MODELS_DIR, '${package}' + proj_settings.MODEL_MODULE_SUFIX + '.py'),
        'Controllers.py_f':pjoin(proj_settings.CONTROLLERS_DIR, '${package}' + proj_settings.CONTROLLER_MODULE_SUFIX + '.py'),
        'Forms_d':pjoin(proj_settings.FORM_MODELS_DIR, '${package}'),
        'Models_d':pjoin(proj_settings.MODELS_DIR, '${package}'),
        'Controllers_d':pjoin(proj_settings.CONTROLLERS_DIR, '${package}'),
        'tests_d':pjoin(proj_settings.TESTS_DIR, '${package}'),
        'docs_d':pjoin(proj_settings.DOCS_DIR, '${package}'),
        'lib_d':pjoin(proj_settings.LIB_DIR,'${package}'),
        'app.py_f':pjoin(proj_settings.APPS_DIR, '${package}.py'),
        #'handlerMap.py':proj_settings.HANDLER_MAP_FILE,
        }
        
    @restrictBaseProjectAccess
    def copyItem(self, src, dest, dType):
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
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
    def __pack__(self, packageName, destination):
        for key in self.packageStructure.keys():
            if key.find('_')>0:
                (destName, dType) = key.split('_')
                dest = pjoin(destination, destName)
                src = Template(self.packageStructure[key]).substitute(package=packageName)
                self.copyItem(src, dest, dType)

    def __unpack__(self, packageName, source):
        projectManager.currentProject.packages.append(packageName)
        for key in self.packageStructure.keys():
            if key.find('_')>0:
                (srcName, dType) = key.split('_')
                src = pjoin(source, srcName)
                dest = Template(self.packageStructure[key]).substitute(package=packageName)
                self.copyItem(src, dest, dType)
            
    @restrictBaseProjectAccess
    def createPackages(self, dirPath, root = proj_settings.PROJ_LOC):
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        tail, head = os.path.split(dirPath)
        skipNum = 0
        if(root in dirPath):
            skipNum =  len(root.split(os.path.sep))
        while head and len(tail.split(os.path.sep))>=skipNum:
            if(not os.path.exists(pjoin(tail, head, '__init__.py'))):
                open(pjoin(tail, head, '__init__.py'), 'w').close()
            tail, head = os.path.split(tail)
        return True

    def pack(self, packageName, destination):
        if os.path.exists(destination):
            if os.path.isdir(destination):
                if ask('Directory Already Exists, All contents will be deleted, Do you want to continue?', input=self.input_method):
                    shutil.rmtree(destination)
                    os.makedirs(destination)
                    self.__pack__(packageName, destination)
                else:
                    return
            else:
                print 'There is file with the same name, Cannot continue!'
                return
        else:
            self.__pack__(packageName, destination)
    @restrictBaseProjectAccess
    def unpack(self, packageName, source):
        if os.path.exists(source):
            self.__unpack__(packageName, source)
        else:
            print 'Such Package does not exist'
    @restrictBaseProjectAccess
    def delete(self, pname):
        print 'This paths will be permanently deleted'
        for key in self.packageStructure.keys():
            if key.find('_')>0:
                destName=dType=''
                destName, dType = key.split('_')
                destName=self.packageStructure[key].replace('${package}', os.path.sep.join(pname.split('.')))
    
                if dType=='d':
                    if os.path.exists(destName):
                        print destName
                        dirtree.tree(destName, ' ', print_files=True, depth=3)
                else:
                    if os.path.exists(destName):
                        print destName
        if ask('Are you sure you want to delete the Package %s?'%pname, input=self.input_method):
            pcks = projectManager.currentProject.packages
            for key in self.packageStructure.keys():
                if key.find('_')>0:
                    destName=dType=''
                    destName, dType = key.split('_')
                    destName=self.packageStructure[key].replace('${package}', os.path.sep.join(pname.split('.')))
                    if dType=='d':
                        if os.path.exists(destName):
                            print 'removing %s directory'%destName
                            shutil.rmtree(destName)
                    else:
                        if os.path.exists(destName):
                            print 'removing %s file'%destName
                            os.remove(destName)
            print 'Package %s was removed'%pname
    @staticmethod
    def listPackages():
        from halicea.lib.projectManager import currentProject
        print [x.keys()[0] for x in currentProject.packages]
        #contr= ["r".replace(proj_settings.CON, new)]
        
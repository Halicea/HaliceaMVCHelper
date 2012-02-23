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
import shutil
import yaml
from os.path import basename, join as pjoin, dirname, abspath
from ioUtils import copy_directory
from consoleHelpers import ask
from config import proj_settings as settings
from config import INSTALL_LOC as rooot
from helpers import DynamicParameters
installPath = pjoin(rooot, 'baseProject')

class ProjectManager(object):
    def __init__(self, project=None):
      self.project=project
    @staticmethod
    def newProject(toPath):
        doCopy = True
        if os.path.exists(toPath):
            overwrite = ask('Path Already Exists!, Do you want to overwrite?')
            if overwrite:
                shutil.rmtree(toPath) #os.makedirs(toPath)
            else:
                doCopy = False
        if doCopy:
            os.makedirs(toPath)
            os.makedirs(pjoin(toPath, 'src'))
            copy_directory(installPath, pjoin(toPath, 'src'), ['.git',], ['.pyc','.InRoot',])
    
            #set app.yaml file
            str = open(pjoin(toPath,'src', 'app.yaml'), 'r').read()
            str = str.replace('baseproject', basename(toPath).lower())
            f = open(os.path.join(toPath,'src', 'app.yaml'), 'w')
            f.write(str)
            f.close()
    
            #set the manage.py File
            str = open(pjoin(rooot, "halicea_manage.py"), 'r').read()
            str = str.replace('{{hal_path}}', rooot)
            f= open(pjoin(toPath,"manage.py"),'w')
            f.write(str)
            f.close()
    
            #set the .halProject File
            str = open(pjoin(rooot, '.halProject'), 'r').read()
            str = str.replace('baseProject', 'src')
            f = open(pjoin(toPath, '.halProject'), 'w')
            f.write(str)
            f.close()
            print 'Project is Created!'
    #Creates Pydev Eclipse project files
    #        str = open(pjoin(toPath, '.project'), 'r').read()
    #        str = str.replace('{{appname}}', basename(toPath))
    #        f = open(os.path.join(toPath, '.project'), 'w')
    #        f.write(str)
    #        f.close()
    #
    #        str = open(pjoin(toPath, '.pydevproject'), 'r').read()
    #        str = str.replace('{{appname}}', basename(toPath))
    #        str = str.replace('{{appengine_path}}', settings.APPENGINE_PATH)
    #        f = open(pjoin(toPath, '.pydevproject'), 'w')
    #        f.write(str)
    #        f.close()
            

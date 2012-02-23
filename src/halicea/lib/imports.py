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
#along with this program.  If not, see <http://www.gnu.org/licenses/>.__doc__ = """
 Importing the settings from the web project
 this is the module that needs to be replaced while testing
 it needs to be called only in the config modueland nowhere else because fo dependencies
"""
import os
from os.path import join as pjoin
from os.path import abspath, dirname

#Where am I: Hals root directory
def __getInstallLoc__():
    return dirname(dirname(abspath(__file__)))
INSTALL_LOC = __getInstallLoc__()

def __getProjectInfo__():
    prj = pjoin(os.getcwd(),'.halProject')
    if not os.path.exists(prj):
        prj = pjoin(INSTALL_LOC, '.halProject')
        result = {'templates':pjoin(INSTALL_LOC, 'Templates'), 'project':pjoin(INSTALL_LOC, 'baseProject')}
    else:
        replacementsDict = {'halweb': INSTALL_LOC,}
        #nix style config file parser with available dictionary replacement of the values
        result = dict(set([(x.split(':')[0].strip(),x.split(':')[1].strip()) for x in \
                          open(prj,'r').readlines() \
                          if x.strip() and x.strip()[0]!='#']))
        for k in result.iterkeys():
            for rk in replacementsDict:
                result[k] = result[k].replace('${'+rk+'}',replacementsDict[rk])
    return abspath(dirname(prj)), result
def __getProjLoc__():
    root, info = __getProjectInfo__()
    return pjoin(root, info['path'])
#Set it up to be from the working directory
PROJ_LOC = __getProjLoc__()
def __getTemplatesLoc__():
    root, info = __getProjectInfo__()
    return pjoin(root, info['templates'])
TEMPLATES_LOC = __getTemplatesLoc__()
#Add the project into the project path


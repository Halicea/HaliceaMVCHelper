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
import os
from os.path import join as pjoin
from config import proj_settings as settings

def LocateControllerModule(packageName):
    return pjoin(settings.CONTROLLERS_DIR, BasePathFromName(packageName)+settings.CONTROLLER_MODULE_SUFIX+'.py')
def LocateModelModule(packageName):
    return pjoin(settings.MODELS_DIR, BasePathFromName(packageName)+settings.MODEL_MODULE_SUFIX+'.py')
def LocateFormModelModule(packageName):
    return pjoin(settings.FORM_MODELS_DIR, BasePathFromName(packageName)+settings.MODEL_FORM_MODULE_SUFIX+'.py')

def LocatePagesDir(packageName):
    return pjoin(settings.PAGE_VIEWS_DIR, BasePathFromName(packageName))
def LocateFormsDir(packageName):
    return pjoin(settings.FORM_VIEWS_DIR, BasePathFromName(packageName))
def BasePathFromName(packageName, sep=os.path.sep, splitter='.'):
    return sep.join(packageName.split(splitter))

def locate(packageName, mvcSegment):
    return eval("Locate"+mvcSegment)(packageName)

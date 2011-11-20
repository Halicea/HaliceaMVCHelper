__doc__ = """
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
        result = dict(set([(x.split('=')[0].strip(),x.split('=')[1].strip()) for x in \
                          open(prj,'r').readlines() \
                          if x.strip()[0]!='#' and x.strip()]))
        for k in result.iterkeys():
            for rk in replacementsDict:
                result[k] = result[k].replace('${'+rk+'}',replacementsDict[rk])
    return abspath(dirname(prj)), result
def __getProjLoc__():
    root, info = __getProjectInfo__()
    return pjoin(root, info['project'])
#Set it up to be from the working directory
PROJ_LOC = __getProjLoc__()
def __getTemplatesLoc__():
    root, info = __getProjectInfo__()
    return pjoin(root, info['templates'])
TEMPLATES_LOC = __getTemplatesLoc__()
#Add the project into the project path


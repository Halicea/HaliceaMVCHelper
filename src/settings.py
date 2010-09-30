'''
Created on Sep 28, 2010

@author: KMihajlov
'''
import os

DEBUG = True
APPENGINE_PATH = 'C:\\DevApps\\google_appengine'

#Directory Structure
MODELS_DIR = os.path.abspath('Models')
VIEWS_DIR = os.path.abspath('Views')
CONTROLLERS_DIR = os.path.abspath('Controllers')

BASE_VIEWS_DIR = os.path.join(VIEWS_DIR, 'bases')
BLOCK_VIEWS_DIR = os.path.join(VIEWS_DIR, 'blocks')
PAGE_VIEWS_DIR = os.path.join(VIEWS_DIR, 'pages')
FORM_VIEWS_DIR = os.path.join(VIEWS_DIR, 'forms')
#End Directory Structure
DEFAULT_OPERATIONS = {'lst':'list', 'shw':'show', 'ins':'insert', 'del':'delete'}
HANDLER_MAP_FILE = 'handlerMap.py'
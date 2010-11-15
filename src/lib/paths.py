import os
import os.path as p
import settings

def GetTemplateDir(template_type): 
    return p.join(settings.PAGE_VIEWS_DIR, template_type.replace('.', p.sep))

def getViewsDict(dir):
    result = {}
    if os.path.exists(dir) and os.path.isdir(dir):
        for f in os.listdir(dir):
            rf = os.path.join(dir, f)
            if os.path.isfile(rf):
                result[f[:f.rindex('.')]] = os.path.abspath(rf)
    return result

def GetBasesDict():
    result = getViewsDict(settings.BASE_VIEWS_DIR)
    return result

def GetBlocksDict():
    result = getViewsDict(settings.BLOCK_VIEWS_DIR)
    return result

def GetFormsDict(dir):
    result = getViewsDict(p.join(settings.FORM_VIEWS_DIR, dir))
    return result

__customBlocksDict__={}
__customFormsDict__={}
__customPagesDict__={}
__customBasesDict__={}
__customBlocksDict__={}

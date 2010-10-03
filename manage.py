import sys
import os
import shutil
import settings
import pprint
from os.path import join as pjoin
from os.path import abspath
from os.path import dirname
from os.path import basename
 
#Template Configuration
TMPL_DIR = 'Templates'
FRMTMPL = pjoin(TMPL_DIR, 'FormTemplates')
OPRTMPL = pjoin(TMPL_DIR, 'OperationTemplates')

MTPath = pjoin(TMPL_DIR, 'ModelTemplate.txt')
VTPath = pjoin(TMPL_DIR, 'ViewTemplate.txt')
CTPath = pjoin(TMPL_DIR, 'ControllerTemplate.txt')

#Set django in pythonpath

sys.path.append(settings.APPENGINE_PATH)
sys.path.append(pjoin(settings.APPENGINE_PATH, 'lib', 'django' ))

###
os.environ['DJANGO_SETTINGS_MODULE']  = 'settings'
from django import template

types ={'txt':'db.TextProperty',
        'str':'db.StringProperty',
        'bln':'db.BooleanProperty',
        'dtm':'db.DateTimeProperty',
        'date':'db.DateProperty',
        'email':'db.EmailProperty',
        'int':'db.IntegerProperty',
        'float':'db.FloatProperty',
        'ref':'db.ReferenceProperty'}

djangoVars = {'ob':'{{', 'cb':'}}', 'os':'{%', 'cs':'%}', }

mvcPaths = {"modelsPath":basename(settings.MODELS_DIR), 
            'viewsPath':basename(settings.VIEWS_DIR), 
            'controlersPath':basename(settings.CONTROLLERS_DIR)}
libDir = 'lib'
inherits_from = 'db.Model'

class Model(object):
    Package = ''
    Name = ''
    References = []
    Properties = []
    InheritsFrom = ''

class Property(object):
    Name = ''
    Type = ''
    Options = None
    Required = 'False'
    Default = None
    
class MVCHelper(object):
    def GetProjectStructure(self):
        pass
    def MakeMVC(self, args):
        operations = [x[0] for x in settings.DEFAULT_OPERATIONS.iteritems() 
                      if x[1].has_key('view') and x[1]['view']]
        templates = [os.path.join(OPRTMPL,settings.DEFAULT_OPERATIONS[x]['method']+'.txt')
                     for x in settings.DEFAULT_OPERATIONS.iterkeys()]
        templates = list(set(templates))

#       print operations
#       print templates
        m = Model()
        #TODO: Validation needs to be added here
        m.Package = raw_input('PackageName: ')
        m.Name = raw_input('ModelName: ')

        m.InheritsFrom = inherits_from
        print 'Enter Property(Press Enter for End)'
        print 'Format', '[Name] [Type] <param1=value param1=value ...>'
        print 'Types', str([k for k in types.iterkeys()])
        i = 0
        print '.'*13+'class '+m.Name+'('+m.InheritsFrom+'):'
        p = True #Do-While
        while p:
            p = raw_input('Property'+str(i)+'>'+'.'*(9-len(str(i))))
            self.SetProperties(p, m)
            i+=1
        
        print self.Render(m, MTPath)
        print "*"*20
        
        print self.Render(m, VTPath, {'operations':templates})
        print "*"*20
        
        methods = map(lambda x: self.Render(m, x), templates)
        print self.Render(m, CTPath, {'methods':methods})
        
        save = raw_input('Save(y/n)>')
        if save.lower()=='y':
            # Model setup
            modelFile = pjoin(settings.MODELS_DIR, m.Package+'Models.py')
            if not os.path.exists(modelFile):
                f = open(modelFile, 'w')
                f.write('import settings\n')
                f.write('from google.appengine.ext.db.djangoforms import ModelForm\n')
                f.write('from google.appengine.ext import db\n')
                f.write('#'*50+'\n')
                f.close()
            f= open(modelFile, 'a')
            f.write(self.Render(m, MTPath))
            f.close()
            # End Model Setup
            #View Setup
            viewFolder = pjoin(settings.PAGE_VIEWS_DIR, m.Package)
            if not os.path.exists(viewFolder): os.makedirs(viewFolder)
            for k in operations:  
                f = open(pjoin(viewFolder, m.Name+'_'+k+'.html'), 'w')
                f.write(self.Render(m, VTPath, {'formTemplate': m.Name+'Form_'+k }))
                f.close()
            #End Views Setup
            #Forms Setup
            formsFolder = os.path.join(settings.FORM_VIEWS_DIR, m.Package)
            if not os.path.exists(formsFolder): os.makedirs(formsFolder)
            for k in operations:
                f = open(os.path.join(formsFolder, m.Name+'Form_'+k+'.html'), 'w')
                print k, 
                f.write(self.Render(m, os.path.join(FRMTMPL, 'FormTemplate_'+k+'.txt'),{'op':k }))
                f.close()
            #End Form Setup
            #Controller Setup
            controllerFile = os.path.join(settings.CONTROLLERS_DIR, m.Package+'Controllers.py')
            if not os.path.exists(controllerFile):
                f = open(controllerFile, 'w')
                f.write('import settings\n')
                f.write('from lib.HalRequestHandler import HalRequestHandler as hrh\n')
                f.write('from lib.decorators import *\n')
                f.write('from google.appengine.ext import db\n')
                f.write('#'*50+"\n")
                f.close()
            f= open(controllerFile, 'a')
            f.write(self.Render(m, CTPath, {'methods':methods}))
            f.close()
            #End Controller Setup
            #Edit HandlerMap
            f = open(settings.HANDLER_MAP_FILE, 'r'); 
            lines=f.readlines(); 
            f.close()
            newlines = []
            inUrlBlock = False
            inImportsBlock = False
            for line in lines:
                if 'block ApplicationControllers' in line:
                    inUrlBlock=True
                if 'block imports' in line:
                    inImportsBlock=True
                if '{%endblock%}' in line.replace(' ','') and inUrlBlock:
                    url='(\'/'+m.Package.replace('.','/')+'/'+m.Name+'\', '+m.Package+'Controllers.'+m.Name+'Controller),'
                    newlines.append(url+'\n')
                    inUrlBlock =False
                if '{%endblock%}' in line.replace(' ','') and inImportsBlock:
                    txt='from '+basename(settings.CONTROLLERS_DIR)+' import '+m.Package+'Controllers'
                    newlines.append(txt)
                    inImportsBlock =False
                newlines.append(line)
            f = open(settings.HANDLER_MAP_FILE, 'w')
            f.writelines(newlines)
            f.close()

    def Render(self, model, templatePath, additionalVars={}):
        
        str = open(templatePath, 'r').read() 
        t = template.Template(str)
        dict = {'m':model}
        dict.update(djangoVars)
        dict.update(mvcPaths)
        dict.update(additionalVars)
        context = template.Context(dict)
        return t.render(context)

    def SetProperties(self, p, model):
        t = p.split(' ')
        if len(t)>1:
            prop = Property()
            prop.Name = t[0]
            prop.Options = []
            if types.has_key(t[1]): 
                prop.Type = types[t[1]]
            else:
                print 'Not valid property type'
                return False
            propStart = 2
            if t[1]=='ref':
                prop.Options.insert(0, t[propStart])
                has_coll_name = reduce(lambda x,y: x==True or 
                                       (x is str and 'collection_name' in x) or 
                                        'collection_name' in y,
                                       t[propStart])
                if not has_coll_name:
                    prop.Options.append('collection_name=\''+prop.Name.lower()+'_'+model.Name.lower()+'s\'')
                propStart+=1
            if len(t)>propStart:
                for op in t[propStart:]:
                    if '=' in op:
                        prop.Options.append(t)
                    else:
                        print 'Not valid Option %s'%op
                        return False
            model.Properties.append(prop)
            return True
        else:
            if len(t)==1 and  t[0]:
                print 'Must provide Type:'
                pprint.pprint(types)
            return False
def NewProject(toPath):
    doCopy = True
    if os.path.exists(toPath):
        overwrite = raw_input('Path Already Exists!, Do you want to overwrite?(y/n):')
        if overwrite == 'y':
            shutil.rmtree(toPath)#os.makedirs(toPath)
        else:
            doCopy = False
    if doCopy:
        fromPath = os.path.dirname(abspath(__file__))
        print fromPath,'=>', toPath
        raw_input()
        shutil.copytree(fromPath, toPath)
        str = open(pjoin(toPath, 'app.yaml'), 'r').read()
        str = str.replace('{{app_toPath}}', basename(toPath).lower())
        f = open(os.path.join(toPath, 'app.yaml'), 'w')
        f.write(str)
        f.close()
        
        str = open(pjoin(toPath, '.project'), 'r').read()
        str = str.replace('{{appname}}', basename(toPath))
        f = open(os.path.join(toPath, '.project'), 'w')
        f.write(str)
        f.close()
        
        str = open(pjoin(toPath, '.pydevproject'), 'r').read()
        str = str.replace('{{appname}}', basename(toPath))
        str = str.replace('{{appengine_path}}', settings.APPENGINE_PATH)
        f = open(os.path.join(toPath, '.pydevproject'), 'w')
        f.write(str)
        f.close()
        
        os.remove(pjoin(toPath, '.InRoot'))
        print 'Project is Created!'
def convertToTemplate(text,input={}):
    result = text
    for k, v in djangoVars.iteritems():
        result=result.replace(v,'{-{'+k+'}-}')
    for k, v in input.iteritems():
        result=result.replace(v,'{-{'+k+'}-}')
    result = result.replace('{-{','{{')
    result = result.replace('}-}','}}')
    return result

def ConvertToReal(text,input={}):
    result = text
    for k, v in djangoVars.iteritems():
        result=result.replace(k, v)
    for k, v in input.iteritems():
        result=result.replace(k, v)
    return result

def GetTextFromPath(filePath):
    templ = ''
    if filePath[-1]==']' and filePath.rindex('[')>0:
        fn= filePath
        lindex = int(fn[fn.rindex('[')+1:fn.rindex(':')])
        rindex = int(fn[fn.rindex(':')+1:-1])
        f = open(filePath[:filePath.rindex('[')], 'r')
        templ = ''.join(f.readlines()[lindex:rindex])
        f.close()
    else:
        templ = open(filePath,'r').read()
    return templ
def ExtractAgrs(paramsList):
    return dict(map(lambda x:(x[:x.index('=')], x[x.index('=')+1:]), paramsList))
def SaveTextToFile(txt, skipAsk=False, skipOverwrite=False):
    save = skipAsk and raw_input('Save to File?(y/n):')
    if save=='y':
        filePath = raw_input('Enter the Path>')
        if os.path.exists(filePath):
            again = True
            while again:
                again = False
                p = skipOverwrite and raw_input('File already Exists, (o)verwrite, (a)ppend, (p)repend or (c)ancel?>')
                if p=='o' or p==False:
                    f = open(filePath, 'w'); f.write(txt); f.close()
                elif p=='a':
                    f = open(filePath, 'a'); f.write(txt); f.close()
                elif p=='p':
                    f = open(filePath, 'r'); txt = txt+'\n'+f.read(); f.close()
                    f = open(filePath, 'w'); f.write(txt); f.close()
                elif p == 'c':
                    pass
                else:
                    print 'Not Valid Command, Options: o, a, p, c lowercase only!'
                    again = True
                    
                if not again and p!='c':
                    print 'File saved at \"%s\"!'%filePath
        else:
            f = open(p, 'w'); f.write(txt); f.close()
        
baseusage = """
Usage haliceamvc.py [projectPath]
Options: [create]
"""
def main(args):
    a = MVCHelper()
    isInInstall = os.path.exists('.InRoot')
    print isInInstall
    if isInInstall:
        if args[0]=='project' and len(args)>1:
            NewProject(args[1])
        else:
            print 'Not a valid command'
        return
    else:
        if args[0]=='mvc':
            a.MakeMVC(None)
        elif args[0]=='run':
            options = ''
            if len(args)>1:
                options = ' '.join(args[1:]) 
            command = pjoin(settings.APPENGINE_PATH, 'dev_appserver.py')+' '+os.path.abspath(os.path.dirname(__file__)+' '+options)
            print command
            os.system(command)
        elif args[0]=='deploy':
            command = pjoin(settings.APPENGINE_PATH, 'appcfg.py')+' update '+os.path.abspath(os.path.dirname(__file__))
            print command
            os.system(command)
        elif args[0]=='console':
            pass
        else:
            print 'Not Valid Command [mvc, run, console]'
        return
    # can do this in install on local mode    
    if args[0]=='new' and len(args)>2:
        if args[1]=='template':
            templ = GetTextFromPath(args[2])
            input=len(args)>3 and ExtractAgrs(args[3:]) or {}
            txt = convertToTemplate(templ, input)
            print txt; print 
            SaveTextToFile(txt)
        elif args[1] =='real':
            templ = GetTextFromPath(args[2])
            input=len(args)>3 and ExtractAgrs(args[3:]) or {}
            txt = ConvertToReal(templ, input)
            print txt; print
            SaveTextToFile(txt)
        else:
            print 'Not valid type for new'
    #        os.system(os.path.join(settings.APPENGINE_PATH, 'dev_appserver.py')+' '+os.pardir(os.path.abspath(__file__))+' --port 8080')
if __name__ == '__main__':
    main(sys.argv[1:])
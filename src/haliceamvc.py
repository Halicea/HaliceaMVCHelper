import sys
import os
import shutil
import settings

# Get django in pythonpath
j = os.path.join
sys.path.append(settings.APPENGINE_PATH)
sys.path.append(j(settings.APPENGINE_PATH, 'lib', 'django' ))
del j
###
os.environ['DJANGO_SETTINGS_MODULE']  = 'settings'
from django import template

types ={'txt':'db.TextProperty',
        'str':'db.StringProperty',
        'bln':'db.BooleanProperty',
        'dtm':'db.DateTimeProperty',
        'date':'db.Dateproperty',
        'email':'db.EmailProperty',
        'int':'db.IntegerProperty',
        'float':'db.FloatProperty',
        'ref':'db.ReferenceProperty'}
djangoVars = {'os':'{%', 'cs':'%}', 'ob':'{{', 'cb':'}}'}

mvcPaths = {"modelsPath":settings.MODELS_DIR, 'viewsPath':settings.VIEWS_DIR, 'controlersPath':settings.CONTROLLERS_DIR}
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
    Options = []
    Required = 'False'
    Default = None
    
class MVCHelper(object):
    def GetProjectStructure(self):
        pass
    def NewProject(self, name):
        if not os.path.exists(name):
            #os.makedirs(name)
            shutil.copytree('ProjectTemplate', name)
            shutil.copytree('Templates', os.path.join(name, 'Templates'))
            shutil.copy('haliceamvc.py', os.path.join(name,'manage.py'))
            shutil.copy('settings.py', os.path.join(name,'settings.py'))
            str = open(os.path.join(name, 'app.yaml'), 'r').read()
            str = str.replace('{{app_name}}', os.path.basename(name).lower())
            f = open(os.path.join(name, 'app.yaml'), 'w')
            f.write(str)
            f.close()
        else:
            print 'Error %s!'%'Path Already Exists!'
    def MakeMVC(self, args):
        m = Model()
        m.Package = raw_input('PackageName: ')
        m.Name = raw_input('ModelName: ')
        p = True #Do-While
        m.InheritsFrom = inherits_from
        print 'Enter Property(Press Enter for End)'
        print 'Format', '[Name] [Type] <param1=value param1=value ...>'
        print 'Types', str([k for k in types.iterkeys()])
        i = 0
        print '.'*13+'class '+m.Name+'('+m.InheritsFrom+'):'
        while p:
            p = raw_input('Property'+str(i)+'>'+'.'*(9-len(str(i))))
            self.SetProperties(p, m)
            i+=1
        print self.Render(m, 'ModelTemplate.txt')
        print "*"*20
        print self.Render(m, 'ViewTemplate.txt')
        print "*"*20
        print self.Render(m, 'ControllerTemplate.txt')
        save = raw_input('Save(y/n)>')
        if save.lower()=='y':
            # Model setup
            modelFile = os.path.join(settings.MODELS_DIR, m.Package+'Models.py')
            if not os.path.exists(modelFile):
                f = open(modelFile, 'w')
                f.write('from google.appengine.ext.db.djangoforms import ModelForm\n')
                f.write('from google.appengine.ext import db\n')
                f.write('#'*50+'\n')
                f.close()
            f= open(modelFile, 'a')
            f.write(self.Render(m, 'ModelTemplate.txt' ))
            f.close()
            # End Model Setup
            #View Setup
            viewFolder = os.path.join(settings.PAGE_VIEWS_DIR, m.Package)
            if not os.path.exists(viewFolder): os.makedirs(viewFolder)
            f = open(os.path.join(viewFolder, m.Name+'_'+k+'.html'), 'w')
            f.write(self.Render(m, 'ViewTemplate.txt'))
            # Make template for each operation
            for k, v in settings.DEFAULT_OPERATIONS.iteritems():
                f = open(os.path.join(viewFolder, m.Name+'_'+k+'.html'), 'w')
                f.write(self.Render(m, 'ViewTemplate.txt', {'formTemplate': m.Name+'Form_'+k }))
            #End Views Setup
            #Forms Setup
            formsFolder = os.path.join(settings.FORM_VIEWS_DIR, m.Package)
            if not os.path.exists(formsFolder): os.makedirs(formsFolder)
            for k, v in settings.DEFAULT_OPERATIONS.iteritems():
                f = open(os.path.join(formsFolder, m.Name+'Form_'+k+'.html'), 'w')
                f.write(self.Render(m, 'FormTemplates/FormTemplate_'+k+'.txt', {'op':k}))
            #End Form Setup
            #Controller Setup
            controllerFile = os.path.join(settings.CONTROLLERS_DIR, m.Package+'Handlers.py')
            if not os.path.exists(controllerFile):
                f = open(controllerFile, 'w')
                f.write('from MyRequestHandler import MyRequestHandler as mrh\n')
                f.write('from google.appengine.ext import db\n')
                f.write('#'*50+"\n")
                f.close()
            f= open(controllerFile, 'a')
            f.write(self.Render(m, 'ControllerTemplate.txt' ))
            f.close()
            #End Controller Setup
        
    def Render(self, model, templateName, additionalVars={}):
        templatePath = os.path.join('Templates', templateName)
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
            if types.has_key(t[1]): 
                prop.Type = types[t[1]]
            else:
                print 'Not valid property type'
                return False
            propStart = 2
            if t[1]=='ref':
                prop.Options.insert(0, t[propStart])
                propStart+=1

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
                print 'Must provide Type:'+types
            return False
baseusage = """
Usage haliceamvc.py [projectPath]
Options: [create]
"""
def main(args):
    a = MVCHelper()
    if args[0]=='mvc':
        a.MakeMVC(None)
    elif args[0]=='project' and len(args)>1:
        a.NewProject(args[1])
    elif args[0]=='run' and len(args)>1:
        command = os.path.join(settings.APPENGINE_PATH, 'dev_appserver.py')+' '+os.path.abspath(os.path.dirname(__file__))+' --port 8080'
        print command
        os.system('cmd %s'%command)
    elif args[0]=='console':
        pass
#        os.system(os.path.join(settings.APPENGINE_PATH, 'dev_appserver.py')+' '+os.pardir(os.path.abspath(__file__))+' --port 8080')
    else:
        print 'Not Valid Command [mvc, run, console]'

if __name__ == '__main__':
    main(sys.argv[1:])
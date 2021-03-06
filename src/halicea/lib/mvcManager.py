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
import pprint
from sys import stdout,stdin
from string import Template
from os import makedirs
import os
from os.path import basename, dirname, join as pjoin, exists
#------------
from consoleHelpers import ask
from config import proj_settings as settings, MvcTemplateDirs
import config, packager
from baseClasses import Model, Property, Block
import locators, mvcPaths
from codeBlocksHelpers import HalCodeBlockLocator, InPythonBlockLocator

class MVCManager(object):
    cblPy = InPythonBlockLocator()
    cblHal = HalCodeBlockLocator()
    
    def __init__(self, project, *args, **kwargs):
        self.operations = [(x[0],x[1]) for x in settings.DEFAULT_OPERATIONS.iteritems()
                  if x[1].has_key('view') and x[1]['view']]
        self.libDir = 'lib'
        self.inherits_from = 'db.Model'
        self.project = project
    
    @staticmethod
    def render(templatePath, context={}):
        templText = open(templatePath, 'r').read()
        t = config.TEMPLATE_RENDERER(templText)
        contextDict ={}
        contextDict.update(context)
        contextDict.update(config.djangoVars)
        contextDict.update(config.mvcPaths)
        contextDict.update(config.sufixesDict)
        return t.render(contextDict)
    
    def setProperties(self, p, model):
        t = p.split(' ')
        if len(t)>1:
            prop = Property()
            prop.Name = t[0]
            prop.Options = []
            if config.types.has_key(t[1]):
                prop.Type = config.types[t[1]]
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
            elif t[1]=='selfref':
                has_coll_name = reduce(lambda x,y: x==True or
                                       (x is str and 'collection_name' in x) or
                                        'collection_name' in y,
                                       t[propStart])
                if not has_coll_name:
                    prop.Options.append('collection_name=\''+prop.Name.lower()+'_'+model.Name.lower()+'s\'')
            if len(t)>propStart:
                for op in t[propStart:]:
                    if '=' in op:
                        prop.Options.append(op)
                    else:
                        print 'Not valid Option %s'%op
                        return False
    #        print model.Properties
            model.Properties.append(prop)
            return True
        else:
            if len(t)==1 and  t[0]:
                print 'Must provide Type:'
                pprint.pprint(config.types)
            return False
    
    def renderModel(self, model=None, baseBlock=None, outputStream=stdout, magicType='magic0', *args):
        MvcTemplateFiles = mvcPaths.getTemplateFiles(magicType)
        baseBlock.appendText(self.render(MvcTemplateFiles['MTPath'], {'m':model}))
        outputStream.write(str(baseBlock))
    
    def renderModelForm(self, model=None, baseBlock=None, outputStream=stdout,magicType='magic0',*args):
        MvcTemplateFiles = mvcPaths.getTemplateFiles(magicType)
        baseBlock.appendText(render(MvcTemplateFiles['FTPath'], {'m':model}))
        outputStream.write(str(baseBlock))
    
    def renderController(self, model=None , baseBlock=None,outputStream=stdout, magicType='magic0', *args):
        MvcTemplateDirs= mvcPaths.getTemplatesDirs(magicType)
        MvcTemplateFiles = mvcPaths.getTemplateFiles(magicType)
        methods = None
        m = model
        if m:
            ops=[]
            if os.path.exists(MvcTemplateDirs['OPRTMPL_DIR']):
                ops = [x[:x.rindex('.')] for x in os.listdir(MvcTemplateDirs['OPRTMPL_DIR'])]
            methodTemplates = []
            for k in ops:
                methodTemplates.append(pjoin(MvcTemplateDirs['OPRTMPL_DIR'],k+'.txt'))
    #NOTICE: We dont need this. most probably we will need to walk thru template files only
    #        and not to make them dependend on the operations
    #        for k, v in settings.DEFAULT_OPERATIONS.iteritems():
    #            if isinstance(v['method'], str):
    #                methodTemplates.append(pjoin(MvcTemplateDirs['OPRTMPL_DIR'],v['method']+'.txt'))
    #            else:
    #                methodTemplates.append(pjoin(MvcTemplateDirs['OPRTMPL_DIR'],v['method'].__name__+'.txt'))
            methodTemplates = list(set(methodTemplates))
    
            methods = map(lambda x: render(x, {'m':m}), methodTemplates)
            classImport = Template('from ${modelsPath}.${modelModule} import ${modelClass}')\
                .substitute(modelsPath=basename(settings.MODELS_DIR),
                            modelModule=m.Package+settings.MODEL_MODULE_SUFIX,
                            modelClass=m.Name)
            formImport = Template('from ${formsPath}.${formModule} import ${formClass}')\
                .substitute(formsPath=basename(settings.FORM_MODELS_DIR),
                        formModule=m.Package+settings.MODEL_FORM_MODULE_SUFIX,
                        formClass=m.Name+settings.MODEL_FORM_CLASS_SUFIX)
            if not baseBlock['imports']:
                baseBlock.createEmptyBlocks('imports', cblPy)
            baseBlock['imports'].appendLines([classImport, formImport])
        baseBlock.appendText(self.render(MvcTemplateFiles['CTPath'], {'m':m, 'methods':methods}))
        outputStream.write(str(baseBlock))
    
    def renderHandlerMap(self, model=None, baseBlock=None,outputStream=stdout, magicType='magic0', *args):
        handlerMap = baseBlock
        appControllers = handlerMap['ApplicationControllers']
        imports = handlerMap['imports']
        m = model
        #Create the block if it does not exists
        blockName = m.Package+settings.CONTROLLER_MODULE_SUFIX
        if not appControllers[blockName]:
            appControllers.createEmptyBlocks(blockName, self.cblPy)
        myBlock = appControllers[blockName]
    
        templ = Template("""('/${model}', ${controller}),""")
        urlEntry =templ.substitute(model=locators.BasePathFromName(m.FullName, '/'),
                                   controller=m.Package+settings.CONTROLLER_MODULE_SUFIX+'.'+m.Name+settings.CONTROLLER_CLASS_SUFIX
                                   )
        myBlock.append(Block.createLineBlock(urlEntry))
    
        importsLine= 'from '+basename(settings.CONTROLLERS_DIR)+' import '+m.Package+settings.CONTROLLER_MODULE_SUFIX
        if not imports[importsLine]:
            imports.append(Block.createLineBlock(importsLine))
        outputStream.write(str(handlerMap))
    
    def makeModelListFromFile(self, modelFile):
        f = open(modelFile, 'r')
        lines = [x.replace('\n','') for x in f.readlines()]
        modelList = []
    
        m=Model()
        print 'Parsing the File '+modelFile
        for line in lines:
            if not m.Name:
                m.Name = line[line.rindex('.')+1:]
                m.Package = line[:line.rindex('.')]
                m.InheritsFrom = inherits_from
            elif line:
                self.setProperties(line, m)
            else:
                modelList.append(m)
                m=Model()
        f.close()
        print 'created Models'+str(modelList)
        return modelList
    
    #TODO make creating a model to a File based object that can be parsed
    def makeModelFromClass(self, fullName):
        raise NotImplementedError("Implement Me")
    def makeModelListFromModule(self, moduleName):
        raise NotImplementedError("Implement Me")
    
    def makeMvc(self, args):
        arg = args[0]
        package = ''
        name =''
        magicLevel = settings.MagicLevel
        modelList = []
        #TODO: set the MagicLevel
        #TODO: make try catch and display proper output if wrong syntax is entered
        if len(args)>1:
            if args[1][:len('path=')]=='path=':
                modelList = self.makeModelListFromFile(args[1][len('path='):])
            else:
                name = args[1][args[1].rindex('.')+1:]
                package = args[1][:args[1].rindex('.')]
        if len(args)>2:
            magicLevel = int(args[2])
        magicType = 'magic'+str(magicLevel)
    
        mvcTemplateFiles = mvcPaths.getTemplateFiles(magicType)
        mvcTemplateDirs = mvcPaths.getTemplatesDirs(magicType)
        if not modelList:
            m = Model()
            #TODO: Validation needs to be added here
            if not (name and package):
                m.Package = ask('PackageName: ', '*')
                m.Name = ask('ModelName: ', '*')
            else:
                m.Package = package
                m.Name = name
    
            if 'm' in arg:
                #TODO: set to according to an argument
                m.InheritsFrom = self.inherits_from
                i = 0
                print '.'*14+'class '+m.FullName+'('+m.InheritsFrom+'):'
                p = True #Do-While
                while p:
                    p = raw_input('Property'+str(i)+'>'+'.'*(9-len(str(i))))
                    if self.setProperties(p, m): i+=1
            else:
                #Create a Model instance out of specific class if exists
                raise NotImplemented('This feature is not implemented yet')
            modelList.append(m)
    
        for m in modelList:
            if ask('Save '+m.FullName+'?'):
                if 'm' in arg:
                    #Model setup
                    modelFile = locators.LocateModelModule(m.Package)
                    baseBlock = None
                    if exists(modelFile):
                        baseBlock = Block.loadFromFile(modelFile, self.cblPy)
                    else:
                        baseBlock =Block.loadFromFile(mvcTemplateFiles["MBTPath"], self.cblPy, self.render, {'m':m})
                    stream = open(modelFile, 'w')
                    self.renderModel(m, baseBlock, stream, magicType=magicType)
                    stream.close()
                    #End Model Setup
                if 'f' in arg:
                    #ModelForm Setup
                    mfPath = locators.LocateFormModelModule(m.Package)
                    baseBlock = None
                    if exists(mfPath):
                        baseBlock = Block.loadFromFile(mfPath, self.cblPy)
                    else:
                        baseBlock = Block.loadFromFile(mvcTemplateFiles['FBTPath'], self.cblPy, self.render, {'m':m})
                    stream = open(mfPath, 'w')
                    self.renderModelForm(m, baseBlock,stream,magicType)
                    stream.close()
                    #End ModelForm Setup
                if 'c' in arg:
                    #Controller Setup
                    controllerPath = locators.LocateControllerModule(m.Package)
                    baseBlock = None
                    if exists(controllerPath):
                        baseBlock = Block.loadFromFile(controllerPath, cblPy)
                    else:
                        baseBlock = Block.loadFromFile(mvcTemplateFiles["CBTPath"], self.cblPy, self.render, {'m':m})
                    stream = open(controllerPath, 'w')
                    self.renderController(m, baseBlock, stream, magicType, arg)
                    stream.close()
                    #End Controller Setup
                if 'v' in arg:
                    viewFolder = locators.LocatePagesDir(m.Package)
                    formFolder =locators.LocateFormsDir(m.Package)
                    #if we only want an empty view
                    if not m:
                        pass
                    #if we want to generate the view by the model provided
                    else:
                        #Find the operations for the templates
                        ops=[]
                        if os.path.exists(mvcTemplateDirs['FRMTMPL_DIR']):
                            ops = [x[:x.rindex('.')] for x in os.listdir(mvcTemplateDirs['FRMTMPL_DIR'])]
                        if ops:
                            for k in ops:
                                templateName = k
                                formTemplatePath = pjoin(mvcTemplateDirs['FRMTMPL_DIR'], templateName+'.txt')
                                viewPath = pjoin(viewFolder, m.Name+'_'+(k=='default' and [''] or [k])[0] +'.html')
                                baseBlock  = Block.loadFromFile(mvcTemplateFiles['VTPath'], self.cblHal, self.render,{'m':m,'formTemplate': m.Name+'Form_'+k })
                                baseBlock.saveToFile(viewPath)
    
                                formPath = pjoin(formFolder, m.Name+settings.FORM_VIEW_SUFFIX+'_'+k+'.html')
                                baseBlock  = Block.loadFromFile(formTemplatePath, self.cblHal, self.render,{'m':m})
                                baseBlock.saveToFile(formPath)
                        else: #here the magic will be used and we dont need some special view
                            viewPath = pjoin(viewFolder, m.Name+'.html')
                            baseBlock  = Block.loadFromFile(mvcTemplateFiles['VTPath'], self.cblHal, self.render,{'m':m})
                            baseBlock.saveToFile(viewPath)
#                if 'h' in arg:
#                    #HandlerMap Setup
#                    baseBlock = Block.loadFromFile(config.proj_settings.HANDLER_MAP_FILE, self.cblPy)
#                    stream = open(config.proj_settings.HANDLER_MAP_FILE, 'w')
#                    self.renderHandlerMap(m, baseBlock, stream, magicLevel)
#                    stream.close()
#                    #End HandlerMap
    
    def delMvc(self, mvc, modelFullName):
        pass

import pprint
from string import Template
from os import makedirs
from os.path import basename, dirname, join as pjoin, exists
#------------
from halicea.consoleHelpers import ask
from halicea.config import proj_settings as settings
from halicea import config
from halicea.baseClasses import Model, Property, Block
from halicea import locators
from halicea.codeBlocksHelpers import HalCodeBlockLocator, InPythonBlockLocator
cblPy = InPythonBlockLocator()
cblHal = HalCodeBlockLocator()

libDir = 'lib'

inherits_from = 'db.Model'
def render(templatePath, context={}):
    str = open(templatePath, 'r').read()
    t = config.TEMPLATE_RENDERER(str)
    contextDict ={}
    contextDict.update(context)
    contextDict.update(config.djangoVars)
    contextDict.update(config.mvcPaths)
    contextDict.update(config.sufixesDict)
    return t.render(contextDict)

def setProperties(p, model):
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

def makeMvc(args):
    arg = args[0]
    package = ''
    name =''
    magicLevel = settings.MagicLevel
    #TODO: set the MagicLevel
    MvcTemplateDirs = {}; MvcTemplateDirs.update(config.MvcTemplateDirs)
    MvcTemplateFiles = {}; MvcTemplateFiles.update(config.MvcTemplateFiles)
    
    #Set the path to the corresponding magic Level
    for k in MvcTemplateDirs.iterkeys():
        MvcTemplateDirs[k]=MvcTemplateDirs[k].replace('{{magicLevel}}', 'magic'+str(magicLevel))
    for k in MvcTemplateFiles.iterkeys():
        MvcTemplateFiles[k]=MvcTemplateFiles[k].replace('{{magicLevel}}', 'magic'+str(magicLevel))
        
    config.TMPL_DIR =config.TMPL_DIR.replace('{{magicLevel}}', 'magic'+str(magicLevel))
    #TODO: make try catch and display proper output if wrong sintax is entered
    if len(args)>1:
        name = args[1][args[1].rindex('.')+1:]
        package = args[1][:args[1].rindex('.')] 

    operations = [x[0] for x in settings.DEFAULT_OPERATIONS.iteritems() 
                  if x[1].has_key('view') and x[1]['view']]

    templates = []
    for k, v in settings.DEFAULT_OPERATIONS.iteritems():
        if isinstance(v['method'], str):
            templates.append(pjoin(MvcTemplateDirs['OPRTMPL_DIR'],v['method']+'.txt'))
        else:
            templates.append(pjoin(MvcTemplateDirs['OPRTMPL_DIR'],v['method'].__name__+'.txt'))
    templates = list(set(templates))

    m = Model()
    #TODO: Validation needs to be added here
    if not (name and package):
        m.Package = ask('PackageName: ', '*')
        m.Name = ask('ModelName: ', '*')
    else:
        m.Package = package
        m.Name = name
    if 'm' in arg:
        m.InheritsFrom = inherits_from
        i = 0
        print '.'*14+'class '+m.FullName+'('+m.InheritsFrom+'):'
        p = True #Do-While
        while p:
            p = raw_input('Property'+str(i)+'>'+'.'*(9-len(str(i))))
            if setProperties(p, m):
                i+=1
        print render(MvcTemplateFiles['MTPath'], {'m':m})
        print "*"*20
    else:
        raise NotImplemented('This feature is not implemented yet')
    if 'v' in arg:
        print render(MvcTemplateFiles['VTPath'],{'m':m,'operations':templates})
        print "*"*20
    if 'c' in arg:
        methods = map(lambda x: render(x, {'m':m}), templates)
        print render(MvcTemplateFiles['CTPath'], {'m':m, 'methods':methods})
    if 'f' in arg:
        print render(MvcTemplateFiles['FTPath'], {'m':m})
    if ask('Save?'):
        if 'm' in arg:
            # Model setup
            modelFile = locators.LocateModelModule(m.Package)
            mb = None
            if not exists(dirname(modelFile)):
                makedirs(dirname(modelFile))
            if not exists(modelFile):
                mb = Block.loadFromFile(MvcTemplateFiles['MBTPath'], cblPy, render, {'m':m})
            else:
                mb = Block.loadFromFile(modelFile, cblPy)
            mb.appendText(render(MvcTemplateFiles['MTPath'], {'m':m}))
            mb.saveToFile(modelFile)
            # End Model Setup
        if 'f' in arg:
            modelFormFile = locators.LocateFormModelModule(m.Package)
            if not exists(dirname(modelFormFile)):
                makedirs(dirname(modelFormFile))
            frmBl = None
            if not exists(modelFormFile):
                frmBl = Block.loadFromFile(MvcTemplateFiles['FBTPath'], cblPy, render,{'m':m})
            else:
                frmBl = Block.loadFromFile(modelFormFile, cblPy)
            frmBl.appendText(render(MvcTemplateFiles['FTPath'], {'m':m}))
            frmBl.saveToFile(modelFormFile)
        if 'v' in arg:
            #View Setup
            viewFolder = locators.LocatePagesDir(m.Package)
            if not exists(viewFolder): makedirs(viewFolder)
            for k in operations:
                Block\
                    .loadFromFile(MvcTemplateFiles['VTPath'],cblHal, render, {'m':m,'formTemplate': m.Name+'Form_'+k })\
                    .saveToFile(pjoin(viewFolder, m.Name+'_'+k+'.html'))

            #Forms Setup
            if magicLevel == 0:
                formsFolder = locators.LocateFormsDir(m.Package)
                if not exists(formsFolder): makedirs(formsFolder)
                for k in operations:
                    Block\
                        .loadFromFile(pjoin(MvcTemplateDirs['FRMTMPL_DIR'], 'FormTemplate_'+k+'.txt'), cblHal, render, {'m':m, 'op':k})\
                        .saveToFile(pjoin(formsFolder, m.Name+'Form_'+k+'.html'))
        if 'c' in arg:
            #Controller Setup
            controllerFile = locators.LocateControllerModule(m.Package)
            cntBl = None
            if not exists(dirname(controllerFile)):
                makedirs(dirname(controllerFile))
            if not exists(controllerFile):
                cntBl =Block.loadFromFile(MvcTemplateFiles['CBTPath'], cblPy, render, {'m':m})
            else:
                cntBl =Block.loadFromFile(controllerFile, cblPy)
            classImport = Template('from ${modelsPath}.${modelModule} import ${modelClass}')\
                .substitute(modelsPath=basename(settings.MODELS_DIR),
                            modelModule=m.Package+settings.MODEL_MODULE_SUFIX,
                            modelClass=m.Name)
            if 'f' in arg:
                formImport = Template('from ${formsPath}.${formModule} import ${formClass}')\
                    .substitute(formsPath=basename(settings.FORM_MODELS_DIR),
                            formModule=m.Package+settings.MODEL_FORM_MODULE_SUFIX,
                            formClass=m.Name+settings.MODEL_FORM_CLASS_SUFIX)
            if 'f' in args:
                cntBl['imports'].appendLines([formImport])
            cntBl['imports'].appendLines([classImport])
            cntBl.appendText(render(MvcTemplateFiles['CTPath'], {'m':m, 'methods':methods}))
            cntBl.saveToFile(controllerFile)
            
            #End Controller Setup
            #Edit HandlerMap
            handlerMap = Block.loadFromFile(settings.HANDLER_MAP_FILE, cblPy)
            appControllers = handlerMap['ApplicationControllers']
            imports = handlerMap['imports']
            #Create the block if it does not exists
            blockName = m.Package+settings.CONTROLLER_MODULE_SUFIX
            if not appControllers[blockName]:
                appControllers.createEmptyBlocks(blockName, cblPy)

            myBlock = appControllers[blockName]
            
            templ = Template("""('/${model}', ${controller}),""")
            urlEntry =templ.substitute(model=locators.BasePathFromName(m.FullName, '/'),
                                       controller=m.Package+settings.CONTROLLER_MODULE_SUFIX+'.'+m.Name+settings.CONTROLLER_CLASS_SUFIX
                                       )
            myBlock.append(Block.createLineBlock(urlEntry))

            importsLine= 'from '+basename(settings.CONTROLLERS_DIR)+' import '+m.Package+settings.CONTROLLER_MODULE_SUFIX
            if not imports[importsLine]:
                imports.append(Block.createLineBlock(importsLine))
            handlerMap.saveToFile(settings.HANDLER_MAP_FILE)
    m=None
def delMvc(mvc, modelFullName):
    pass
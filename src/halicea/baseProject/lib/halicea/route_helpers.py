import os
import inspect
from conf.settings import CONTROLLER_CLASS_SUFIX
from conf.settings import CONTROLLER_EXTENSTION
from conf.settings import CONTROLLER_MODULE_SUFIX
from conf.settings import PROJ_LOC
from conf.settings import CONTROLLERS_DIR
from lib.halicea.helpers import ClassImport, NotSuportedException
from pprint import pprint
def get_controllers(directory, include_module=False, include_package=False):
  result = {}
  directory = directory.replace('\\', '/')
  rootPackage = directory[len(PROJ_LOC):]
  
  if rootPackage.endswith('/'):
    rootPackage=rootPackage[:-1]
  if rootPackage.startswith('/'):
    rootPackage=rootPackage[1:]
    
  for root, dirs, files in os.walk(directory):
    root = root.replace('\\', '/')
    package = root[len(directory):]
    if package.endswith('/'):
      package = package[:-1]
    if package.startswith('/'):
      package = package[1:]
    
    for f in files:
      if f.endswith(CONTROLLER_MODULE_SUFIX+CONTROLLER_EXTENSTION):
        info = inspect.getmoduleinfo(os.path.join(root, f))
        module = '.'.join([x for x in [rootPackage, package, info.name] if x])
        try:
          base = __import__(module, fromlist=['.'.join([x for x in [rootPackage, package] if x])])
          for name in [x for x in dir(base) if x.endswith(CONTROLLER_CLASS_SUFIX)]:
            obj = getattr(base, name)
            if inspect.isclass(obj):
              name_c =name[:-len(CONTROLLER_CLASS_SUFIX)].lower()
              package_c= package.lower()
              module_c = module[module.rindex('.')+1:][:-len(CONTROLLER_MODULE_SUFIX)].lower()
              
              if include_module:
                name_c = module_c+'/'+name_c
              if include_package and package_c:
                name_c = package_c+'/'+name_c
                
              result[name_c]= '.'.join([module, name])
        except Exception, ex:
          pprint(ex)
  return result

class HalActionDispatcher(object):
  def dispatch(self, controller, *args, **kwargs):
    action_func = controller.operations[controller.op or 'default']['method']
    if isinstance(action_func, str):
      if '.' in action_func:
        action_func = ClassImport(action_func)
      else:
        action_func = getattr(controller, action_func)
      if not action_func:
        raise Exception("Invalid action")
    elif not callable(action_func):
      raise NotSuportedException("Only string and callabels are accepted as Controller action arguments. Instead %s found."%str(type(action_func)))
    
    if inspect.ismethod(action_func):
      return action_func(*args, **kwargs)
    else:
      action_func(controller, *args, **kwargs)
      
if __name__=='__main__':
  import conf.imports
  from pprint import pprint
  result = get_controllers(CONTROLLERS_DIR)
  pprint(result)
  print "="*20
  result = get_controllers(CONTROLLERS_DIR, True)
  pprint(result)
  print "="*20
  result = get_controllers(CONTROLLERS_DIR, True, True)
  pprint(result)
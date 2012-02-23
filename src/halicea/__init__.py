from lib.config import proj_settings as settings
from lib.helpers import DynamicParameters
from os.path import join as pjoin, dirname
import yaml
__currentProject__ =None
def get_current_project():
  pkg= yaml.load(open(pjoin(dirname(settings.PROJ_LOC), '.halPackages'),'r').read()) or {}
  prj = yaml.load(open(pjoin(dirname(settings.PROJ_LOC), '.halProject'),'r').read())
  result = DynamicParameters(prj)
  result.packages = DynamicParameters(pkg)
  return result
  
  
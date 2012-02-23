from tests.testImports import *
from unittest import TestCase
from lib.halicea.route_helpers import get_controllers
from conf.settings import CONTROLLERS_DIR
from lib.routes import Mapper
from lib.routes.util import URLGenerator as urlc
from conf.handlerMap import webapphandlers
class RoutesTest(TestCase):
  @classmethod
  def setUpClass(cls):
    cls.mapper = Mapper(get_controllers(CONTROLLERS_DIR)) 
    cls.mapper.extend(webapphandlers)
  @classmethod
  def tearDownClass(cls):
    super(RoutesTest, cls).tearDownClass()
  
  def test_1_Url(self):
    url = urlc(RoutesTest.mapper, {'HTTP_HOST':'localhost'})
    print url('login')
    print url('logout')
    print url(controller='base', action='index')
    
    
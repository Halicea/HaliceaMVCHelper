# -*- coding: utf-8 -*-
from conf.settings import DEBUG, EXTENSIONS, COOKIE_KEY
from conf.handlerMap import webapphandlers
from lib.halicea.HalBaseHandler import HalBaseHandler
from lib.halicea.wsgi import WSGIApplication
from lib.gaesessions import SessionMiddleware
#register Extensions
HalBaseHandler.extend(*EXTENSIONS)
#end
app = SessionMiddleware(
        WSGIApplication(webapphandlers, debug=DEBUG), 
        COOKIE_KEY)

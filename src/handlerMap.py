# -*- coding: utf-8 -*-
import os
import settings
os.environ['DJANGO_SETTINGS_MODULE']  = 'settings'
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from lib.gaesessions import SessionMiddleware

#{%block imports%}
from Controllers import BaseControllers, ShellControllers
from Controllers import StaticControllers
#{%endblock%}

#Definition of the Controller Url mappings
application = webapp.WSGIApplication(
[
#('/', TestControllers.TestController),
#{%block ApplicationControllers %}
#{% block BaseControllers %}
('/Login', BaseControllers.LoginController),
('/Logout',BaseControllers.LogoutController),
('/AddUser', BaseControllers.AddUserController),
('/WishList', BaseControllers.WishListController),
('/admin/Role', BaseControllers.RoleController),
('/admin/RoleAssociation', BaseControllers.RoleAssociationController),
('/Base/WishList', BaseControllers.WishListController),
#{%endblock%}

#{%block StaticControllers%}
('/',StaticControllers.WelcomeController),
('/Contact', StaticControllers.ContactController),
('/About', StaticControllers.AboutController),
('/Links', StaticControllers.LinksController),
('/NotAuthorized', StaticControllers.NotAuthorizedController),
#{%endblock%}
#{%block ShellControllers%}
('admin/Shell', ShellControllers.FrontPageController),
('admin/Shell/Statement', ShellControllers.StatementController),
#{%endblock%}
#{%endblock%}
('/(.*)', StaticControllers.NotExistsController),
], debug=settings.DEBUG)
COOKIE_KEY = '''2zÆœ;¾±þ”¡j:ÁõkçŸÐ÷8{»Ën¿A—jÎžQAQqõ"bøó÷*%†™ù¹b¦$vš¡¾4ÇŸ^ñ5¦'''
def webapp_add_wsgi_middleware(app):
    from google.appengine.ext.appstats import recording
    app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
    app = recording.appstats_wsgi_middleware(app)
    return app

def main():
    run_wsgi_app(webapp_add_wsgi_middleware(application))

if __name__ == "__main__":
    main()
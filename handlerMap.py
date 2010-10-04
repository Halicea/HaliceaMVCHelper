from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from lib.gaesessions import SessionMiddleware

# {% block imports %}
from Controllers import baseControllers
from Controllers import staticControllers
# {% endblock %}

#"""Load custom Django template filters"""
#webapp.template.register_template_library('lib.customFilters')

debug=True
application = webapp.WSGIApplication(
[
 ##########
 ('/', staticControllers.WelcomeController),
 #{% block ApplicationControllers %}
 #{% endblock %}
 #{% block baseControllers %}
 ('/Login', baseControllers.LoginController),
 ('/Logout', baseControllers.LogoutController),
 ('/AddUser', baseControllers.AddUserController),
 ('/WishList', baseControllers.WishListController),
 #{%endblock%}
 
 #{%block staticControllers%}
 ('/Links', staticControllers.LinksController),
 ('/NotAuthorized', staticControllers.NotAuthorizedController),
 #{%endblock%}
 ('/(.*)', staticControllers.NotExistsController),
], debug=debug)
def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app)
    return app
def main():
	run_wsgi_app(\
					 webapp_add_wsgi_middleware(application)\
					)

if __name__ == "__main__":
	main()

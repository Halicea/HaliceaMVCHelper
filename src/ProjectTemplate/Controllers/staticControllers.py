'''
Created on Oct 16, 2007

@author: Kosta
'''
from MyRequestHandler import MyRequestHandler as mrh
handlerType='static'

class AboutController( mrh ):
	def get( self ):
		self.respond()

class LinksController( mrh ):
	def get( self ):
		self.respond()

class WelcomeController(mrh):
	def get(self):
		self.respond()

class ContactController( mrh ):
	def get( self ):
		self.respond()
		
class NotExistsController( mrh ):
	def get( self, page_address ):
		if self.request.get('ajax'):
			self.response.out.write("Ajax navigate to wrong address!")
		else:
			self.respond()

class NotAuthorizedController( mrh ):
	def get(self):
		self.response.out.write("""
		<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
			<html>
				<head>
					<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
					<title>UnAuthorized Page</title>
				</head>
				<body>
					<div align="center">
						<h2><font color="red">You are not authorized to view this resource!</font> </h2>
					<a href="/">Home</a><br>
					<a href="/Login">Login</a>	
					</div>
				</body>
			</html>
		""")
	def post(self):
		self.response.out.write("""
		<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
			<html>
				<head>
					<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
					<title>UnAuthorized Page</title>
				</head>
				<body>
					<div align="center">
						<h2><font color="red">You are not authorized to view this resource!</font> </h2>
					<a href="/">Home</a><br>
					<a href="/Login">Login</a>	
					</div>
				</body>
			</html>
		""")

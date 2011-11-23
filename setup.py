from setuptools import setup, find_packages
import os
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
print find_packages('src')
setup(name="HalWeb",
      version='0.5.5',
      description='Halicea Web Framework(HalWeb) is an Appengine MVC web framework for real easy, understandable and rapid development',
      long_description=read('README'),
      author='Costa Halicea',
      author_email ='costa@halicea.com',
      url='http://halweb.halicea.com',
      package_dir = {'':'src'},
      scripts = ['src/halicea/hal.py', 'src/halicea/halicea_manage.py'],
      packages= find_packages('src'),
      #modules=['hal.py', 'halicea_manage.py'],
      keywords = "gae appengine framework google python web halicea halweb",
      zip_safe = False,
      include_package_data = True,
      classifiers=[
             'Development Status :: 4 - Beta',
             'Environment :: Console',
             'Environment :: Web Environment',
             'Intended Audience :: Developers',
             'License :: OSI Approved :: Python Software Foundation License',
             'Operating System :: MacOS :: MacOS X',
             'Operating System :: Microsoft :: Windows',
             'Operating System :: POSIX',
             'Programming Language :: Python',
             'Programming Language :: Python :: 2.5',
             'Programming Language :: Python :: 2.6',
             'Programming Language :: Python :: 2.7',
             'Topic :: Internet',
             'Topic :: Internet :: WWW/HTTP :: WSGI',
             'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
             'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
             'Topic :: Software Development',
             'Topic :: Software Development :: Code Generators',
             'Topic :: Software Development :: Libraries :: Application Frameworks',
             'Topic :: Software Development :: Libraries :: Python Modules',
             'Topic :: Text Processing :: Markup :: HTML',
          ],
      entry_points={
	'console_scripts': [
            'hal = hal:real_main',
            #'halicea = hal:real_main',
        ]
	},
    )



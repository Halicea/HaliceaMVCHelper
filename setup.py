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
      version='0.1.2',
      description='Halicea Web Framework is an MVC Like web framework focused primarily for Appengine development',
      long_description=read('README'),
      author='Costa Halicea',
      author_email ='costa@halicea.com',
      url='http://halweb.halicea.com',
      package_dir = {'':'src'},
      scripts = ['src/halicea/hal.py', 'src/halicea/halicea_manage.py'],
      packages= find_packages('src'),
      #modules=['hal.py', 'halicea_manage.py'],
      keywords = "appengine framework google halicea python web halweb",
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
          'Topic :: Communications :: Email',
          'Topic :: Software Development :: Google App Engine',
          ],
      entry_points={
	'console_scripts': [
            'hal = hal:real_main',
            #'halicea = hal:real_main',
        ]
	},
    )



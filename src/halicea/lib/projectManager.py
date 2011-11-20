import os, shutil
from os.path import basename, join as pjoin, dirname, abspath
from ioUtils import copy_directory
from consoleHelpers import ask
from config import proj_settings as settings
from config import INSTALL_LOC as rooot
installPath = pjoin(rooot, 'baseProject')
def newProject(toPath):
    doCopy = True
    if os.path.exists(toPath):
        overwrite = ask('Path Already Exists!, Do you want to overwrite?')
        if overwrite:
            shutil.rmtree(toPath) #os.makedirs(toPath)
        else:
            doCopy = False
    if doCopy:
        os.makedirs(toPath)
        os.makedirs(pjoin(toPath, 'src'))
        copy_directory(installPath, pjoin(toPath, 'src'), ['.git',], ['.gitignore','.pyc','.InRoot',])

        #set app.yaml file
        str = open(pjoin(toPath,'src', 'app.yaml'), 'r').read()
        str = str.replace('{{appname}}', basename(toPath).lower())
        f = open(os.path.join(toPath,'src', 'app.yaml'), 'w')
        f.write(str)
        f.close()

        #set the manage.py File
        str = open(pjoin(rooot, "halicea_manage.py"), 'r').read()
        str = str.replace('{{hal_path}}', rooot)
        f= open(pjoin(toPath,"manage.py"),'w')
        f.write(str)
        f.close()

        #set the .halProject File
        str = open(pjoin(rooot, '.halProject'), 'r').read()
        str = str.replace('baseProject', 'src')
        f = open(pjoin(toPath, '.halProject'), 'w')
        f.write(str)
        f.close()
#Creates Pydev Eclipse project files
#        str = open(pjoin(toPath, '.project'), 'r').read()
#        str = str.replace('{{appname}}', basename(toPath))
#        f = open(os.path.join(toPath, '.project'), 'w')
#        f.write(str)
#        f.close()
#
#        str = open(pjoin(toPath, '.pydevproject'), 'r').read()
#        str = str.replace('{{appname}}', basename(toPath))
#        str = str.replace('{{appengine_path}}', settings.APPENGINE_PATH)
#        f = open(pjoin(toPath, '.pydevproject'), 'w')
#        f.write(str)
#        f.close()

        if os.path.exists(pjoin(toPath, 'halicea.py')):
            os.rename(pjoin(toPath,'halicea.py'), pjoin(toPath,'manage.py'))

        print 'Project is Created!'

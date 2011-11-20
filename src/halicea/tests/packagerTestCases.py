import unittest
import os
from os.path import join as pjoin
import shutil
import sys
import test_imports
sys.modules['imports'] = test_imports
globals()['imports']= test_imports
locals()['imports']= test_imports
#imports is needed for the initial configuration of the project
#the path of the project is given there and well as the path of the templates directory

from halicea.lib import packager
resDir = os.path.join(os.path.dirname(__file__), 'resources')

def displayIOError( *args, **kwargs ):
    print args, kwargs

class PackageTestCases(unittest.TestCase):
    repo_orig = None
    proj_orig = None
    repo =None
    proj =None
    @classmethod
    def setUpClass(cls):      
        cls.proj = pjoin(resDir,'testProjectV1_Actual')
        cls.repo = pjoin(resDir,'TestRepository_Actual')
        cls.repo_orig = pjoin(resDir, 'testRepository')
        cls.proj_orig = pjoin(resDir, 'testProjectV1')
        shutil.copytree(pjoin(resDir,'testProjectV1'),cls.proj)
        shutil.copytree(pjoin(resDir,'TestRepository'),cls.repo)
        
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.proj, False, displayIOError)
        shutil.rmtree(cls.repo, False, displayIOError)

    def test_pack_if_package_exists_in_repo(self):
        pack = packager.Packager(lambda *args: 'y')
        pack.pack('Base', pjoin(self.repo, 'ExistingPackage'))
        #Model is copied
        expected = open(pjoin(self.proj_orig, 'Models','BaseModels.py'), 'r').read()
        actual = open(pjoin(self.repo, 'ExistingPackage','Models.py'), 'r').read()
        self.assertEqual(actual, expected, "Models are not equal")

        #Controller is copied
        expected = open(pjoin(self.proj_orig, 'Controllers','BaseControllers.py'), 'r').read()
        actual = open(pjoin(self.repo, 'ExistingPackage','Controllers.py'), 'r').read()
        self.assertEqual(actual, expected, "Controllers are not equal")
    
    def test_pack_if_package_does_not_exist_in_repo(self):
        pack = packager.Packager(lambda *args: 'y')
        pack.pack('Base', pjoin(self.repo, 'NotExistingPackage'))
        #Model is copied
        expected = open(pjoin(self.proj_orig, 'Models','BaseModels.py'), 'r').read()
        actual = open(pjoin(self.repo, 'NotExistingPackage','Models.py'), 'r').read()
        self.assertEqual(actual, expected, "Models are not equal")
        
        #Controller is copied
        expected = open(pjoin(self.proj_orig, 'Controllers','BaseControllers.py'), 'r').read()
        actual = open(pjoin(self.repo, 'NotExistingPackage','Controllers.py'), 'r').read()
        self.assertEqual(actual, expected, "Controllers are not equal")

#    def test_pack_if_not_package_exists(self):
#        pass

    def test_unpack(self):
        pack = packager.Packager(lambda *args: 'y')
        pack.unpack('ToUnpack', pjoin(self.repo, 'ToUnpack'))
        self.assertTrue(os.path.exists(pjoin(self.proj,'Models','ToUnpackModels.py')), "Models module is missing")
        self.assertTrue(os.path.exists(pjoin(self.proj,'Controllers','ToUnpackControllers.py')), "Controllers module is missing")
    
    def test_delete(self):
        pack = packager.Packager(lambda *args: 'y')
        pack.delete('Base')
        self.assertFalse(os.path.exists(pjoin(self.proj,'Models','BaseModels.py')), "Models module should be deleted")
        self.assertFalse(os.path.exists(pjoin(self.proj,'Controllers','BaseControllers.py')), "Controllers module should be deleted")
    
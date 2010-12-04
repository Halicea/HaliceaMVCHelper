import unittest
import os
from os.path import join as pjoin
import shutil
from halicea import packager
resDir = os.path.join(os.path.dirname(__file__), 'resources')

class PackageTestCases(unittest.TestCase):
    def setUp(self):
        pass
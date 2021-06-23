import unittest

from test.base.files_mixin import FilesMixIn
from test.base.pathcers import patch_config_path
from test.base.fixtures import *

from main import Application


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Application()


class IntegratedTestCase(FilesMixIn, BaseTestCase):
    pass

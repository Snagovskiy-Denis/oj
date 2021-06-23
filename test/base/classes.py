import unittest

from test.base.files_mixin import FilesMixIn
from main import Application


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Application()


class IntegratedTestCase(FilesMixIn, BaseTestCase):
    pass

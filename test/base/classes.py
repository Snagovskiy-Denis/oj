import unittest

from test.base.files_mixin import FilesMixIn
from test.base.patchers import patch_config_path
import test.base.fixtures as f

from main import Application


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Application()


class IntegratedTestCase(FilesMixIn, BaseTestCase):
    '''Creates test environment to satisfy external dependencies

    Class creates test files for path-resolving functional and
    patch Configurator._get_config_path to read created config.
    '''
    files_to_create = (f.TEMPLATE, f.CONFIG)

    def setUp(self):
        self.create_files()
        self.config_path_patcher = patch_config_path()
        self.mock_config_path = self.config_path_patcher.start()
        super().setUp()

    def tearDown(self):
        self.config_path_patcher.stop()


class FunctionalTest(IntegratedTestCase):
    pass

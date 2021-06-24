import datetime
import unittest
from unittest.mock import patch

from test.base.files_mixin import FilesMixIn
import test.base.fixtures as f
from paths import BASE_DIRECTORY

from main import Application


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Application()


class IntegratedTestCase(FilesMixIn, BaseTestCase):
    '''Creates test environment to satisfy external dependencies

    List of external dependencies:

        * files: config, template (optionally destination file)
        * today's date
        * environment variables
        * system arguments

    Class creates test files for path-resolving functional and
    patch Configurator._get_config_path to read created config.
    '''
    files_to_create = (f.TEMPLATE, f.CONFIG)

    def setUp(self):
        self.create_files()

        self.config_path_patcher = patch(
                'configurator.Configurator._get_config_path', 
                return_value=self.files[f.CONFIG].path)
        self.todays_date_patcher = patch('datetime.date', 
                **{'today.return_value': datetime.date(2012, 12, 21)})
        self.getenv_patcher = patch('main.getenv', return_value='vi')
        self.sys_argv_patcher = patch('sys.argv', 
                [BASE_DIRECTORY.joinpath('main.py')])

        self.mock_config_path = self.config_path_patcher.start()
        self.mock_todays_date = self.todays_date_patcher.start()
        self.mock_getenv = self.getenv_patcher.start()
        self.sys_argv_mock = self.sys_argv_patcher
        super().setUp()

    def tearDown(self):
        self.config_path_patcher.stop()
        self.todays_date_patcher.stop()
        self.getenv_patcher.stop()
        self.sys_argv_patcher.stop()


class FunctionalTest(IntegratedTestCase):
    pass

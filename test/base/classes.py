import unittest
from datetime import date
from unittest.mock import patch

import test.base.fixtures as f
from constants import TEST_DIRECTORY

from test.base.files_mixin import FilesMixIn
from test.base.system_mixin import SystemMixIn

from oj import Application


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Application()


class IntegratedTestCase(FilesMixIn, SystemMixIn, BaseTestCase):
    '''Creates test environment to satisfy external dependencies

    List of external dependencies:

        * files: config, template (optionally destination file)
        * today's date
        * environment variables
        * system arguments
        * file writing
        * process running

    Class creates test files for path-resolving functional and
    patch Configurator._get_config_path to read created config.
    Afterwards it patchs todas date, env variables and sysargv.
    '''
    files_to_create = (f.TEMPLATE, f.CONFIG)

    def setUp(self):
        self.initiate_test_environment()
        super().setUp()

    def tearDown(self):
        self.clear_test_environment()

    def initiate_test_environment(self):
        self.create_files()
        self.create_fake_date_and_expected_path()
        self.isolate_from_system()

        self.config_path_patcher = patch(
                'configurator.Configurator._get_config_path', 
                return_value=self.files[f.CONFIG].path)
        self.mock_config_path = self.config_path_patcher.start()

    def clear_test_environment(self):
        self.stop_system_isolation()

        self.config_path_patcher.stop()
        self.date_patcher.stop()

    def create_fake_date_and_expected_path(self):
        fake_date_str = f.FAKE_DATE.isoformat() + f.EXTENSION

        self.expected_path = TEST_DIRECTORY.joinpath(fake_date_str)
        self.date_patcher = patch('oj.date', 
                **{'today.return_value': f.FAKE_DATE})
        self.mock_date = self.date_patcher.start()

import os
import sys
import unittest
import datetime
from pathlib import Path
from unittest.mock import Mock, patch

from test.base.classes import IntegratedTestCase 
from test.base.pathcers import patch_sys_argv, patch_config_path
from test.base.fixtures import *

from constants import DESTINATION, TEMPLATE, DATE_FORMAT


class FirstLaunchTest(IntegratedTestCase):
    files_to_create = (FIXTURE_TEMPLATE, FIXTURE_CONFIG)

    @patch_config_path()
    @patch_sys_argv(('main.py',))
    def test_launch_without_sys_args_with_default_settings_creates_new_note(
                self, mock_config_path
            ):
        # Script is being executed
        # It finds that there is only script pathname in sysargv
        # There is only script pathname in system arguments
        # Because of that Script chooses default default behaviour mode
        self.assertEqual(self.app.get_mode(), 'DEFAULT')

        # Secondly it checks if configuration file exist and reads it
        self.assertTrue(self.files[FIXTURE_CONFIG].path.is_file())
        self.assertEqual(len(self.app.configurations), 0)

        self.app.read_config_file()
        settings = self.app.configurations

        # There are default settings values for:
        #   * destination path
        #   * template path
        #   * filenames' date format
        default_settings = {
                DESTINATION: sys.argv[0].parent.joinpath('test'),
                TEMPLATE: self.files[FIXTURE_TEMPLATE].path,
                DATE_FORMAT: '%Y-%M-%D',
            }
        for setting, expected_value in default_settings.items():
            self.assertIn(setting, settings.keys())
            self.assertEqual(expected_value, settings[setting])

        # It checks that default settings are valid and finds that:
        #   * could build filename with given date format
        filename = '2021-12-21.md'
        destination = default_settings[DESTINATION].joinpath(filename)

        mock_date = Mock(wraps=datetime.date)
        mock_date.today.return_value = datetime.date(2012, 12, 21)
        with patch('datetime.date', new=mock_date):
            self.app.build_filename()

        self.assertEqual(destination, self.app.destination())

        #   * destination file does not exist yet
        #   * destination path is writable
        self.assertFalse(destination.is_file())
        self.assertTrue(os.access(default_settings[DESTINATION], os.W_OK))

        self.assertTrue(self.app.is_destination_valid())

        #   * template path file is exist and readable
        self.assertTrue(Path(default_settings[TEMPLATE]).is_file())
        self.assertTrue(os.access(default_settings[TEMPLATE], os.W_OK))

        self.assertEqual(expected, self.app.is_template_valid())

        # It creates markdown file on destination path
        #   * Files' filename is todays date in setting format

        #   * Files content identical to file on template path

        # It opens file in EDITOR described in environment variable
        self.fail('finish me!')


if __name__ == '__main__':
    unittest.main()

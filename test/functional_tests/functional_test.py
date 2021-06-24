import datetime
import os
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

import test.base.fixtures as f
from test.base.classes import FunctionalTest
from test.base.patchers import patch_sys_argv, patch_config_path

from constants import DEFAULT_MODE, DESTINATION, TEMPLATE, DATE_FORMAT


class FirstLaunchTest(FunctionalTest):
    @patch_sys_argv(('main.py',))
    def test_launch_without_sys_args_with_default_settings_creates_new_note(
                                                                    self):
        # Script is being executed
        # It finds that there is only script pathname in sysargv
        # There is only script pathname in system arguments
        # Because of that Script chooses default default behaviour mode
        self.assertEqual(self.app.get_mode(), DEFAULT_MODE)

        # Secondly it checks if configuration file exist and reads it
        self.assertTrue(self.files[f.CONFIG].path.is_file())
        self.assertEqual(len(self.app.configurations), 0)

        self.app.read_config_file()
        settings = self.app.configurations

        # There are default settings values for:
        #   * destination path
        #   * template path
        #   * filenames' date format
        default_settings = {
                DESTINATION: f.TEST_DIRECTORY,
                TEMPLATE: self.files[f.TEMPLATE].path,
                DATE_FORMAT: f.DATE_FORMAT,
            }
        for setting, expected_value in default_settings.items():
            self.assertIn(setting, settings.keys())
            self.assertEqual(expected_value, settings[setting])

        # It checks that default settings are valid and finds that:
        #   * files' name is todays date
        #   * date is formated by given date format
        filename = '2012-12-21.md'
        destination = default_settings[DESTINATION].joinpath(filename)

        config = {'today.return_value': datetime.date(2012, 12, 21)}
        with patch('datetime.date', **config):
            self.app.build_filename()

        self.assertEqual(destination.name, self.app.destination.name)
        self.assertEqual(destination, self.app.destination)

        #   * destination file does not exist yet
        #   * destination path is writable
        self.assertFalse(self.app.destination.exists())
        self.assertTrue(os.access(f.TEST_DIRECTORY, os.W_OK), 
            "Test have not write access to directory:\n{f.TEST_DIRECTORY}")

        #   * can read template file on given path
        self.assertTrue(Path(default_settings[TEMPLATE]).is_file())
        self.assertTrue(os.access(default_settings[TEMPLATE], os.R_OK),
            "Test have not read access on path:\n{f.TEST_DIRECTORY}")

        self.assertEqual(self.app.template, '')
        self.app.read_template_file()
        self.assertEqual(self.app.template, self.files[f.TEMPLATE].data)

        # It creates markdown file on destination path
        #   * files content identical to file on template path
        with patch('pathlib.Path.write_text') as mock_write_text:
            self.app.create_note()
            mock_write_text.assert_called_once_with(
                         self.files[f.TEMPLATE].data)

        # It opens file in EDITOR described in environment variable

        # TODO last step of this test
        self.fail('finish me!')
        with patch('subprocess') as mock_subprocess:
            self.app.open_note()


if __name__ == '__main__':
    unittest.main()

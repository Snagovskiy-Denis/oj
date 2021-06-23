import pathlib
import sys
import unittest
from unittest.mock import patch

from test.base.classes import IntegratedTestCase 
from test.base.pathcers import patch_sys_argv, patch_config_path


class FirstLaunchTest(IntegratedTestCase):
    files_to_create = ('template', 'config')

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
        self.assertTrue(self.files['config'].path.is_file())
        self.assertEqual(len(self.app.configurations), 0)

        self.app.read_config_file()
        settings = self.app.configurations

        # There are default settings values for:
        #   * destination path
        #   * template path
        #   * filenames' date format
        default_settings = {
                'destination': sys.argv[0].parent.joinpath('test'),
                'template': self.files['template'].path,
                'date format': '%Y-%M-%D',
            }
        for setting, expected_value in default_settings.items():
            self.assertIn(setting, settings.keys())
            self.assertEqual(expected_value, settings[setting])

        # It checks that default settings are valid and finds that:
        #   * destination file does not exist yet
        #   * destination path is writable

        #   * template path file is exist and readable

        #   * date format is valid

        # It creates markdown file on destination path
        #   * Files' filename is todays date in setting format

        #   * Files content identical to file on template path

        # It opens file in EDITOR described in environment variable
        self.fail('finish me!')


if __name__ == '__main__':
    unittest.main()

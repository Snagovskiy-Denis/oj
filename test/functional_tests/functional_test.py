import sys
import unittest
from unittest.mock import patch, call

from main import Application


class FirstLaunchTest(unittest.TestCase):
    """Open jopen for the first time"""
    def setUp(self):
        self.app = Application()

    def tearDown(self):
        pass

    def test_launch_without_sys_args_with_default_settings_creates_new_note(
                self
                ):
        # Script is being executed
        # It finds that there is only script pathname in sysargv
        # There is only script pathname in system arguments
        sys.argv = ['script_path']
        self.assertEquals(len(sys.argv), 1)
        self.assertEquals(sys.argv[0], 'script_path')

        # Because of that Script chooses default default behaviour mode
        self.assertEquals(self.app.get_mode(), 'DEFAULT')

        # Secondly it checks if configuration init file exist 
        # and reads it
        settings = self.app.read_config_file()

        # There are default settings values for:
        #   * destination path
        #   * template path
        #   * filenames' date format
        default_settings = ('', '', '')  # patch this
        destination_path, template_path, date_formay = default_settings

        self.assertIn(default_settings, settings)

        # It checks are default settings valid and finds that:
        #   * destination path file is alredy exist 
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

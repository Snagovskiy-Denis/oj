from configparser import ConfigParser
import pathlib
import sys
import unittest
from unittest import skip
from unittest.mock import patch

from constants import DEFAULT
from test.base.classes import FilesMixIn, BaseTestCase
from test.base.pathcers import patch_sys_argv, patch_config_path, build_path
from exceptions import SectionReadError, SettingReadError


def get_corrupted_config_file():
    config = ConfigParser()
    config['DEFAULT'] = {
            'date format': '%%Y-%%M-%%D',
            'template path': '',
            }
    config['PATH'] = {}
    config['FILENAME'] = {}
    return config


class ApplicationBehaviorSelectionTest(BaseTestCase):
    @patch_sys_argv(('main.py',))
    def test_get_mode_with_one_sys_argument_set_default_mode(self):
        current_mode = self.app.get_mode()
        self.assertEqual(DEFAULT, current_mode)

    @patch_sys_argv(('main.py',))
    def test_remember_mode_if_number_of_sys_arguments_changed(self):
        initial_mode = self.app.get_mode()

        sys.argv = ['argument'] * 5
        current_mode = self.app.get_mode()
        self.assertEqual(initial_mode, current_mode)

    @skip
    def test_get_mode_with_three_or_more_sys_arguments_raise_exception(self):
        sys.argv = ['script_path', 'mode', 'unknown_argument']
        current_mode = self.app.get_mode()
        self.assertEqual(DEFAULT, current_mode)


@patch_config_path()
class ConfiguratorTest(FilesMixIn, BaseTestCase):
    files_to_create = ('template', 'config')

    def test_searches_config_file_in_dunder_file_directory_path(self, _):
        expected_settings: 'destination, date format, template' = [
                build_path(['test']),
                '%Y-%M-%D',
                self.files['template'].path
        ]

        actual_settings = self.app.read_config_file()

        for setting in expected_settings:
            self.assertIn(setting, actual_settings.values())

    @skip
    def test_path_settings_converts_to_Path_class(self):
        pass


class ConfiguratorErrorsTest(BaseTestCase):
    @patch('pathlib.Path.is_file', return_value=False)
    def test_raises_error_if_config_not_found(self, mock_config_filename):
        with self.assertRaises(FileNotFoundError):
            self.app.read_config_file()

    @patch('pathlib.Path.is_file', return_value=True)
    @patch('configparser.ConfigParser.read', return_value='')
    def test_raises_error_if_config_is_empty(self, _, __):
        with self.assertRaises(ValueError):
            self.app.read_config_file()

    @patch('pathlib.Path.is_file', return_value=True)
    @patch('configparser.ConfigParser.sections', return_value=['foo'])
    def test_raises_error_if_can_not_find_section_in_config(self, _, __):
        with self.assertRaises(SectionReadError):
            self.app.read_config_file()

    @patch('configparser.ConfigParser.has_section', return_value=True)
    @patch('pathlib.Path.is_file', return_value=True)
    @patch('configparser.ConfigParser.sections', return_value=['foo', 'bar'])
    def test_raises_error_if_can_not_find_setting_in_section(self, _, _2, _3):
        with self.assertRaises(SettingReadError):
            self.app.read_config_file()


if __name__ == '__main__':
    unittest.main()

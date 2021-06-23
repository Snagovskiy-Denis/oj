from configparser import ConfigParser
import unittest
from unittest import skip
from unittest.mock import patch

from test.base.classes import FilesMixIn, BaseTestCase
from test.base.pathcers import patch_config_path, patch_is_file
from test.base.fixtures import *

from paths import build_path
from exceptions import SectionReadError, SettingReadError


@patch_config_path()
class ConfiguratorTest(FilesMixIn, BaseTestCase):
    files_to_create = (FIXTURE_TEMPLATE, FIXTURE_CONFIG)

    def test_searches_config_file_in_dunder_file_directory_path(self, _):
        expected_settings: 'destination, date format, template' = [
                TEST_DIRECTORY,
                '%Y-%M-%D',
                self.files[FIXTURE_TEMPLATE].path
        ]

        self.app.read_config_file()
        actual_settings = self.app.configurations

        for setting in expected_settings:
            self.assertIn(setting, actual_settings.values())

    @skip
    def test_path_settings_converts_to_Path_class(self):
        pass


@patch('configparser.ConfigParser.sections', return_value=['foo'])
@patch_is_file(return_value=True)
class ConfiguratorErrorsTest(BaseTestCase):
    def test_raises_error_if_config_not_found(
                self, mock_is_file, mock_sections
            ):
        mock_is_file.return_value = False

        with self.assertRaises(FileNotFoundError):
            self.app.read_config_file()

        mock_is_file.assert_called_once()
        mock_sections.assert_not_called()

    @patch('configparser.ConfigParser.read', return_value='')
    def test_raises_error_if_config_is_empty(
                self, mock_read, mock_is_file, mock_sections
            ):
        mock_sections.return_value = []

        with self.assertRaises(ValueError):
            self.app.read_config_file()

        expected_path = str(build_path((FIXTURE_CONFIG,)))

        for mock in mock_is_file, mock_sections:
            mock.assert_called_once()
        mock_read.assert_called_once_with(expected_path)

    def test_raises_error_if_can_not_find_section_in_config(
                self, mock_is_file, mock_sections
            ):
        with self.assertRaises(SectionReadError):
            self.app.read_config_file()

        for mock in mock_is_file, mock_sections:
            mock.assert_called_once()

    @patch('configparser.ConfigParser.has_section', return_value=True)
    def test_raises_error_if_can_not_find_setting_in_section(
                self, mock_has_section, mock_is_file, mock_sections
            ):
        with self.assertRaises(SettingReadError):
            self.app.read_config_file()

        sections = mock_sections.return_value

        mock_has_section.assert_called_once_with(sections[0])
        for mock in mock_is_file, mock_sections:
            mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()

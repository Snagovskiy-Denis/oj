from configparser import ConfigParser
import unittest
from unittest import skip
from unittest.mock import patch

from .base import ConfiguratorTestCase

from exceptions import SectionReadError, SettingReadError


class ConfiguratorTest(ConfiguratorTestCase):
    def test_searches_config_file_in_dunder_file_directory_path(self):
        expected = self.create_configurations()
        self.assertIncludeSettings(expected, self.configurator.read())

    @skip
    def test_converts_path_settings_from_str_to_Path_class(self):
        pass

    @skip
    def test_raises_error_if_cannot_convert_path_setting_from_string_to_Path(
            self, mock_sections):
        self.fail('Expected failure')


@patch('configparser.ConfigParser.sections', return_value=['foo'])
class ConfiguratorErrorsTest(ConfiguratorTestCase):

    @patch('pathlib.Path.is_file', return_value=False)
    def test_raises_error_if_config_not_found(
                self, mock_is_file, mock_sections
            ):
        self.config_path_patcher.stop()

        with self.assertRaises(FileNotFoundError):
            self.configurator.read()

        mock_is_file.assert_called_once()
        mock_sections.assert_not_called()

    @patch('configparser.ConfigParser.read', return_value='')
    def test_raises_error_if_config_is_empty(self, mock_read, mock_sections):
        mock_sections.return_value = []

        with self.assertRaises(ValueError):
            self.configurator.read()

        mock_sections.assert_called_once()
        mock_read.assert_called_once_with(self.config_file.path)

    def test_raises_error_if_can_not_find_section_in_config(
                self, mock_sections
            ):
        with self.assertRaises(SectionReadError):
            self.configurator.read()

        mock_sections.assert_called_once()

    @patch('configparser.ConfigParser.has_section', return_value=True)
    def test_raises_error_if_can_not_find_setting_in_section(
                self, mock_has_section, mock_sections
            ):
        with self.assertRaises(SettingReadError):
            self.configurator.read()

        sections = mock_sections.return_value

        mock_has_section.assert_called_once_with(sections[0])
        mock_sections.assert_called_once()

    @skip
    def test_raises_error_if_required_setting_is_missed_in_config_file(
            self, mock_sections):
        self.fail('Expected failure')



if __name__ == '__main__':
    unittest.main()

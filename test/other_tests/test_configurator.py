from configparser import ConfigParser
from pathlib import Path
import unittest
from unittest import skip
from unittest.mock import Mock, patch

from .base import ConfiguratorTestCase

from constants import DESTINATION


class ValidConfigFileTestCase(ConfiguratorTestCase):
    def test_searches_config_file_in_dot_config_if_default_settings(self):
        self.config_path_patcher.stop()

        with patch('pathlib.Path.is_file', return_value=True) as mock_is_file:
            self.configurator.read()

        mock_is_file.assert_called_once()

    @skip
    def test_all_options_apart_from_paths_have_defaults_values(self):
        pass

    def test_converts_path_section_options_from_str_to_Path(self):
        settings = self.configurator.read()
        path = settings.getpath(DESTINATION)

        self.assertIsInstance(path, Path)
        self.assertEqual(path, self.destination_directory)


class InvalidConfigFileTestCase(ConfiguratorTestCase):
    @skip
    def test_raises_error_if_required_setting_is_missed_in_config_file(self):
        self.fail('Expected failure')


@patch('pathlib.Path.is_file', return_value=False)
class NoConfigFileTestCase(ConfiguratorTestCase):
    config_file_required = False

    def test_raises_error_if_config_file_not_found(self, mock_is_file):
        self.config_path_patcher.stop()

        with self.assertRaises(FileNotFoundError):
            self.configurator.read()
            mock_is_file.assert_called_once()


class ConfiguratorErrorsTest(ConfiguratorTestCase):
    @patch('configparser.ConfigParser.sections', return_value=list())
    def test_raises_error_if_config_is_empty(self, mock_sections):
        with self.assertRaises(ValueError):
            self.configurator.read()
            mock_sections.assert_called_once()


if __name__ == '__main__':
    unittest.main()

from pathlib import Path
import unittest
from unittest import skip
from unittest.mock import Mock, patch

from .base import ConfiguratorTestCase

from configurator import DEFAULTS, DESTINATION


class ValidConfigFileTestCase(ConfiguratorTestCase):
    def test_searches_config_file_in_dot_config_if_default_settings(self):
        self.config_path_patcher.stop()

        with patch('configparser.ConfigParser.read') as mock_read:
            with patch('pathlib.Path.is_file') as mock_is_file:
                mock_is_file.return_value=True
                self.configurator.read()

        mock_is_file.assert_called_once()
        config_path = Path().home().joinpath('.config', 'oj.ini')
        mock_read.assert_called_once_with(config_path)

    def test_converts_path_section_options_from_str_to_Path(self):
        settings = self.configurator.read()
        path = settings.get_path(DESTINATION)

        self.assertIsInstance(path, Path)
        self.assertEqual(path, self.destination_directory)

    def test_expand_tilde_as_home_directory_in_path_section_options(self):
        tilde_path = {DESTINATION: '~/test'}
        settings = self.configurator.read(cli_options=tilde_path)
        self.assertEqual(Path().home().joinpath('test'),
                         settings.get_path(DESTINATION))

    def test_default_values_are_read_before_config_file(self):
        defaults = {'date_format': '%%Y-%%m-%%d', 'extension': '.txt',
                'destination': '', 'template': ''}

        with patch('configurator.Configurator.read') as mock_read:
            mock_read.side_effect = self.assertIncludeSettings(
                    defaults, self.configurator)
            self.configurator.read()

    def test_additional_options_used_instead_of_config_file_ones(self):
        additional_options = {'date_format': '%%d/%%m/%%Y', 'extension': ''}
        self.configurator.read(cli_options=additional_options)

        self.assertEqual('%d/%m/%Y', 
                self.configurator.get_in_filename('date_format'))
        self.assertEqual('', self.configurator.get_in_filename('extension'))

    @skip
    def test_additional_options_are_read_last(self):
        pass


@patch('pathlib.Path.is_file', return_value=False)
class NoConfigFileTestCase(ConfiguratorTestCase):
    config_file_required = False

    def setUp(self):
        super().setUp()
        self.config_path_patcher.stop()  # unblock ._get_config_path

    def test_warn_user_if_no_config_is_provided(self, mock_is_file):
        with patch('time.sleep'), self.assertWarns(UserWarning) as w:
            self.configurator.read()

        mock_is_file.assert_called_once()
        self.assertEqual(len(w.warnings), 1)

    def test_give_user_time_to_read_displayed_warning(self, mock_is_file):
        with patch('time.sleep') as mock_sleep, self.assertWarns(UserWarning):
            self.configurator.read()

        mock_is_file.assert_called_once()
        wait_time = int(DEFAULTS['DEFAULT']['wait'])
        mock_sleep.assert_called_once_with(wait_time)

    def test_skip_warning_message_if_skip_parametr(self, _):
        try:
            with patch('time.sleep'), self.assertWarns(UserWarning) as w:
                    self.configurator.read(skip=True)
        except AssertionError:
            pass  # should not raise
        else:
            self.fail('Warning message is not skipped')

    def test_use_PWD_directory_as_distanation_path(self, _):
        self.config_path_patcher.start()
        self.configurator.read()
        self.assertEqual(Path().cwd(),self.configurator.get_path(DESTINATION))

    def test_additional_options_overwrite_default_ones(self, _):
        additional_options = {'date_format': '%%d/%%m/%%Y', 'extension': ''}
        defaults = {'date_format': '%%Y-%%m-%%d', 'extension': '.txt',
                'destination': '', 'template': ''}

        with patch('time.sleep'), self.assertWarns(UserWarning):
            self.configurator.read(cli_options=additional_options)

        self.assertEqual('%d/%m/%Y',
                self.configurator.get_in_filename('date_format'))
        self.assertEqual('',
                self.configurator.get_in_filename('extension'))


if __name__ == '__main__':
    unittest.main()

import datetime
import os
import sys
import unittest
from unittest import skip
from unittest.mock import Mock, patch, call

from test.base.classes import BaseTestCase, IntegratedTestCase
from test.base.patchers import patch_sys_argv, patch_config_path
import test.base.fixtures as f

from constants import (DEFAULT_MODE, REWRITE_MODE, EDITOR,
                       DATE_FORMAT, DESTINATION, TEMPLATE, EXTENSION,
                      )
from paths import TEST_DIRECTORY, NON_EXISTING_PATH 


class ApplicationBehaviorSelectionTest(BaseTestCase):
    @patch_sys_argv(('main.py',))
    def test_get_mode_with_one_sys_argument_set_DEFAULT_mode(self):
        current_mode = self.app.get_mode()
        self.assertEqual(DEFAULT_MODE, current_mode)

    @patch_sys_argv(('main.py',))
    def test_remember_mode_if_number_of_sys_arguments_changed(self):
        initial_mode = self.app.get_mode()

        sys.argv = [sys.argv[0]] * 5
        current_mode = self.app.get_mode()
        self.assertEqual(initial_mode, current_mode)

    @skip
    def test_get_mode_with_three_or_more_sys_arguments_raise_exception(self):
        sys.argv = ['script_path', 'mode', 'unknown_argument']
        current_mode = self.app.get_mode()
        self.assertEqual(DEFAULT_MODE, current_mode)


@patch('datetime.date', **{'today.return_value': datetime.date(2012, 12, 21)})
class ApplicationFilenameValidationTest(IntegratedTestCase):
    def assertInDestinationPath(self, path_name:str):
        datetime.date.today.assert_called_once()
        expected = TEST_DIRECTORY.joinpath(path_name)
        self.assertEqual(expected, self.app.destination)

    def test_builds_destination_with_filename_in_isoformat_date(self, _):
        self.app.build_filename()
        self.assertInDestinationPath('2012-12-21.md')

    def test_builds_destination_with_filename_with_custom_date_format(
                                                    self, _):
        self.files[f.CONFIG].replace_in_data(
                '%%Y-%%m-%%d', '%%d.%%m.%%Y')
        self.app.build_filename()
        self.assertInDestinationPath('21.12.2012.md')

    @skip
    def test_is_destination_valid_with_valid_destination(self, _):
        destination = TEST_DIRECTORY.joinpath('2012-12-21.md')
        mock_destination = Mock(return_value=destination)
        self.app.destination = mock_destination

        self.assertTrue(self.app.is_destination_valid())
        mock_destination.called_with()


class ApplicationTemplateTest(IntegratedTestCase):
    def test_reads_template_file_if_it_exists(self):
        self.assertEqual(self.app.template, '')
        self.app.read_template_file()
        self.assertEqual(self.app.template, self.files[f.TEMPLATE].data)

    def test_raises_error_if_template_file_does_not_exist_on_path(self):
        del self.files[f.TEMPLATE]
        with self.assertRaises(FileNotFoundError):
            self.app.read_template_file()


@patch('pathlib.Path.write_text')
class ApplicationWriteNewNoteTest(BaseTestCase):
    def test_writes_if_destination_path_does_not_exist(self, mock_write_text):
        template = f'{__class__.__name__} test template body'
        self.app.destination = TEST_DIRECTORY.joinpath('2012-12-21.md')
        self.app.template = template

        self.app.create_note()
        mock_write_text.assert_called_once_with(template)

    def test_do_not_write_if_destination_path_exists(self, mock_write_text):
        self.app.destination = TEST_DIRECTORY
        self.app.create_note()
        self.assertEqual(self.app.get_mode(), DEFAULT_MODE)
        mock_write_text.assert_not_called()

    def test_writes_if_REWRITE_mode_and_destination_path_does_not_exist(
                self, mock_write_text
            ):
        self.app.destination = TEST_DIRECTORY.joinpath(NON_EXISTING_PATH)
        self.app.create_note()
        mock_write_text.assert_called_once()


    def test_writes_if_REWRITE_mode_and_destination_path_exitsts(
                self, mock_write_text
            ):
        template = f'{__class__.__name__} test template body'
        self.app.mode = REWRITE_MODE
        self.app.destination = TEST_DIRECTORY
        self.app.template = template

        self.app.create_note()

        mock_write_text.assert_called_once_with(template)


@patch('subprocess.run')
@patch('main.chdir')
@patch('main.getenv', return_value='vi')
class ApplicationOpenNoteTest(BaseTestCase):
    def test_cd_to_destination_path_and_run_editor_on_note_file(
                self, mock_getenv, mock_chdir, mock_run
            ):
        destination = TEST_DIRECTORY.joinpath('2012-12-21.md')
        self.app.destination = destination 

        self.app.open_note()

        mock_chdir.assert_called_once_with(destination)
        mock_getenv.assert_called_once_with(EDITOR)
        mock_run.assert_called_once_with(
                            [mock_getenv.return_value, destination])

    def test_raises_error_if_EDITOR_env_variable_unset(
                self, mock_getenv, mock_chdir, mock_run
            ):
        mock_getenv.return_value = None
        with self.assertRaises(AttributeError):
            self.app.open_note()
        mock_chdir.assert_not_called()
        mock_getenv.assert_called_once_with(EDITOR)
        mock_run.assert_not_called()


if __name__ == '__main__':
    unittest.main()

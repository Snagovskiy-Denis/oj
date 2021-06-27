import sys
import unittest
from unittest import skip
from unittest.mock import Mock, patch, call

from .base import BaseApplicationTestCase, IntegratedApplicationTestCase
from test.environment.fixture_files import TEST_DIRECTORY

from constants import (DEFAULT_MODE, REWRITE_MODE, EDITOR,
                       DATE_FORMAT, DESTINATION, TEMPLATE, EXTENSION,
                      )


@patch('sys.argv', [TEST_DIRECTORY.joinpath('oj.py')])
class ApplicationBehaviorSelectionTest(BaseApplicationTestCase):
    def test_get_mode_with_one_sys_argument_set_DEFAULT_mode(self):
        current_mode = self.app.get_mode()
        self.assertEqual(DEFAULT_MODE, current_mode)

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


class ApplicationFilenameValidationTest(IntegratedApplicationTestCase):
    def assertInDestinationPath(self, path_name: str):
        self.mock_date.today.assert_called_once()
        expected = self.destination_directory.joinpath(path_name)
        self.assertEqual(expected, self.app.destination)

    def test_builds_destination_with_filename_in_isoformat_date(self):
        self.app.configurations = self.create_configurations()
        self.app.build_filename()
        self.assertInDestinationPath('2012-12-21.md')

    def test_builds_destination_with_filename_with_custom_date_format(self):
        self.app.configurations = self.create_configurations(
                date_format='%d.%m.%Y')
        self.app.build_filename()
        self.assertInDestinationPath('21.12.2012.md')


class ApplicationTemplateTest(IntegratedApplicationTestCase):
    # template_file_required = False

    def test_reads_template_file_if_it_exists(self):
        self.app.template = ''
        self.app.configurations = {TEMPLATE: self.template_file.path}

        self.app.read_template_file()

        self.assertEqual(self.app.template, self.template_file.data)

    def test_raises_error_if_template_file_does_not_exist_on_path(self):
        self.app.configurations = {TEMPLATE: self.template_file.path}
        self.delete_file(self.template_file)
        with self.assertRaises(FileNotFoundError):
            self.app.read_template_file()


@patch('pathlib.Path.write_text')
class ApplicationWriteNewNoteTest(BaseApplicationTestCase):
    def test_writes_if_destination_path_does_not_exist(self, mock_write_text):
        template = f'{__class__.__name__} test template body'
        self.app.destination = TEST_DIRECTORY.joinpath(
                '2012-12-21.md')
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
        self.app.destination = TEST_DIRECTORY.joinpath('I_AM_A_LIE.py')
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


class ApplicationOpenNoteTest(IntegratedApplicationTestCase):
    def test_cd_to_destination_path_and_run_editor_on_note_file(self):
        destination = TEST_DIRECTORY.joinpath('2012-12-21.md')
        self.app.destination = destination

        self.app.open_note()

        self.assertFileWasOpened(destination)

    def test_raises_error_if_EDITOR_env_variable_unset(self):
        self.mock_getenv.return_value = None
        with self.assertRaises(AttributeError):
            self.app.open_note()
        self.mock_chdir.assert_not_called()
        self.mock_getenv.assert_called_once_with(EDITOR)
        self.mock_subprocess_run.assert_not_called()


if __name__ == '__main__':
    unittest.main()

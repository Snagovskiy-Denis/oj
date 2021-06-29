from unittest import main
from unittest.mock import patch

from .base import BaseApplicationTestCase, IntegratedApplicationTestCase
from test.environment.fixture_files import TEST_DIRECTORY

from oj import DEFAULT_MODE, REWRITE_MODE, EDITOR


class FilenameValidationTest(IntegratedApplicationTestCase):
    def assertInDestinationPath(self, path_name: str):
        self.mock_date.today.assert_called_once()
        expected = self.destination_directory.joinpath(path_name)
        self.assertEqual(expected, self.app.destination)

    def test_builds_destination_with_filename_in_isoformat_date(self):
        self.app.configurator = self.create_configurations(
            date_format='%%Y-%%m-%%d')
        self.app.build_filename()
        self.assertInDestinationPath('2012-12-21.md')

    def test_builds_destination_with_filename_with_custom_date_format(self):
        self.app.configurator = self.create_configurations(
            date_format='%%d.%%m.%%Y')
        self.app.build_filename()
        self.assertInDestinationPath('21.12.2012.md')


class ApplicationTemplateTest(IntegratedApplicationTestCase):
    config_file_required = False

    def test_reads_template_file_if_it_exists(self):
        self.app.configurator = self.create_configurations(
            template=self.template_file.path)
        self.app.read_template_file()
        self.assertEqual(self.app.template, self.template_file.data)

    def test_return_empty_string_if_can_not_find_template_file(self):
        self.app.configurator = self.create_configurations(
            template='')
        self.delete_file(self.template_file)

        self.app.read_template_file()

        self.assertEqual(self.app.template, '')


@patch('pathlib.Path.write_text')
class ApplicationWriteNewNoteTest(BaseApplicationTestCase):
    def test_writes_if_destination_path_does_not_exist(self, mock_write_text):
        template = f'{__class__.__name__} test template body'
        self.app.template = template
        self.app.destination = TEST_DIRECTORY.joinpath('2012-12-21.md')

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
    main()

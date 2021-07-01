from datetime import date
from unittest import main, skip
from unittest.mock import patch, MagicMock
import io

from .base import BaseApplicationTestCase, IntegratedApplicationTestCase
from test.environment.fixture_files import TEST_DIRECTORY

from configurator import Configurator, CONFIG_DIRECTORY
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

        self.app.create_file_on_destination()

        mock_write_text.assert_called_once_with(template)

    def test_do_not_write_if_destination_path_exists(self, mock_write_text):
        self.app.destination = TEST_DIRECTORY

        self.app.create_file_on_destination()

        self.assertEqual(self.app.get_mode(), DEFAULT_MODE)
        mock_write_text.assert_not_called()

    def test_writes_if_REWRITE_mode_and_destination_path_does_not_exist(
                self, mock_write_text
            ):
        self.app.destination = TEST_DIRECTORY.joinpath('I_AM_A_LIE.py')
        self.app.create_file_on_destination()
        mock_write_text.assert_called_once()


    def test_writes_if_REWRITE_mode_and_destination_path_exitsts(
                self, mock_write_text
            ):
        template = f'{__class__.__name__} test template body'
        self.app.mode = REWRITE_MODE
        self.app.destination = TEST_DIRECTORY
        self.app.template = template

        self.app.create_file_on_destination()

        mock_write_text.assert_called_once_with(template)


class ApplicationOpenNoteTest(IntegratedApplicationTestCase):
    def test_cd_to_destination_path_and_run_editor_on_note_file(self):
        destination = TEST_DIRECTORY.joinpath('2012-12-21.md')
        self.app.destination = destination

        self.app.open_destination()

        self.assertFileWasOpened(destination)

    def test_raises_error_if_EDITOR_env_variable_unset(self):
        self.mock_getenv.return_value = None

        with self.assertRaises(AttributeError):
            self.app.open_destination()

        self.mock_chdir.assert_not_called()
        self.mock_getenv.assert_called_once_with(EDITOR)
        self.mock_subprocess_run.assert_not_called()


# rewrite this file later with addition of extra-template file
class HolidayFeature(IntegratedApplicationTestCase):
    def test_expand_template_text_if_feature_is_on_and_today_is_a_holiday(
                self
            ):
        self.mock_date.today.return_value = MagicMock(spec=date, 
                **{'weekday.return_value': 5})  # today is a holiday
        self.app.configurator = self.create_configurations(
                holiday_on=True, holiday_path=True)

        self.app.read_template_file()
        self.assertIn('[PATH]', self.app.template)

    def test_do_not_expand_template_if_feature_is_on_and_today_is_not_holiday(
                self
            ):
        self.app.configurator = self.create_configurations(
                holiday_on=True, holiday_path=True)
        # extra template = config_file
        self.delete_file(self.config_file)

        self.app.read_template_file()
        self.assertNotIn('[PATH]', self.app.template)

    def test_do_not_expand_template_if_holiday_feature_is_off(self):
        self.mock_date.today.return_value = MagicMock(spec=date, 
                **{'weekday.return_value': 5})  # today is a holiday
        self.app.configurator = self.create_configurations(
                holiday_on=False)

        self.app.read_template_file()

        self.assertNotIn('[PATH]', self.app.template)

    @patch('sys.argv', [__file__, '--skip'])
    def test_do_not_expand_template_text_if_extra_path_do_not_exist(self):
        self.mock_date.today.return_value = MagicMock(spec=date, 
                **{'weekday.return_value': 5})  # today is a holiday
        self.app.configurator = self.create_configurations(
                holiday_on=True, holiday_path=True)
        # extra template = config_file
        self.delete_file(self.config_file)

        self.app.read_template_file()

        self.assertNotIn('[PATH]', self.app.template)


class ConfigSystemArgumentTestCase(IntegratedApplicationTestCase):
    '''oj < echo y > /dev/null

    Beware! Eats all input and output (including pbd)!
    '''
    def setUp(self):
        super().setUp()
        self.config_path_patcher.stop()
        self.app.configurator = Configurator(set_defaults=True)

        config_directory = self.app.configurator.get_path(CONFIG_DIRECTORY)
        self.config_file_path = config_directory.joinpath('oj.ini')

        self.config_read_patch = patch('configparser.ConfigParser.read')
        self.stdout_patch = patch('sys.stdout', new_callable=io.StringIO)
        self.user_input_patch = patch('builtins.input', return_value='y')
        self.is_file_patch = patch('oj.Path.is_file', return_value=False)

        self.mock_config_read = self.config_read_patch.start()
        self.mock_stdout = self.stdout_patch.start()
        self.mock_user_input = self.user_input_patch.start()
        self.mock_is_file = self.is_file_patch.start()
    
    def tearDown(self):
        self.config_read_patch.stop()
        self.stdout_patch.stop()
        self.user_input_patch.stop()
        self.is_file_patch.stop()
        super().tearDown()


class ConfigIfFIleExist(ConfigSystemArgumentTestCase):
    def test_opens_config_file_if_it_exists(self):
        self.mock_is_file.return_value = True

        self.app.config_run()

        self.mock_write_text.assert_not_called()
        self.assertFileWasOpened(self.config_file_path)
    

class ConfigIfFIleDoesNotExist(ConfigSystemArgumentTestCase):
    def test_input_function_called_if_config_file_does_not_exist(self):
        self.app.config_run()
        self.assertIn('/.config/oj.ini', self.mock_stdout.getvalue())
        self.mock_user_input.assert_called_once()

    def test_exit_if_n_user_input(self):
        self.mock_user_input.return_value = 'n'

        self.app.config_run()

        self.mock_write_text.assert_not_called()
        self.mock_chdir.assert_not_called()
        self.mock_subprocess_run.assert_not_called()

    def test_repeat_user_input_if_it_is_not_y_or_n(self):
        self.mock_user_input.side_effect = 'howdy', 'anyone?', 'n'

        self.app.config_run()

        self.assertEqual(len(self.mock_user_input.mock_calls), 3)

    def test_create_config_file_if_it_does_not_exist_and_y_user_input(self):
        default_config_text = Configurator().get_default_config()
        with patch('pathlib.Path.exists', return_value=False):
            self.app.config_run()

        self.mock_write_text.assert_called_once_with(default_config_text)
        self.assertFileWasOpened(self.config_file_path)


if __name__ == '__main__':
    main()

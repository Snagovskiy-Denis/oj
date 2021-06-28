import warnings
from unittest import main
from unittest.mock import patch
from pathlib  import Path

from .base import FunctionalTest

from configurator import DESTINATION, TEMPLATE, DATE_FORMAT, EXTENSION


class FirstRunTest(FunctionalTest):
    config_file_required   = False
    template_file_required = True

    def test_run_with_valid_settings_creates_new_note(self):
        # John has downloaded oj
        # He wants to create new note by his template
        self.assertFileExists(self.template_file)

        # John checks documentation and finds that he needs config file 
        # 
        # He writes new config file with valid settings:
        #   * path to directory where he wants to store his notes
        #   * path to template file for new notes
        #   * ISO 8601 as desired date format
        #   * markdown extension
        john_settings = {
                DESTINATION: Path(__file__).parent.parent,
                TEMPLATE: self.template_file.path,
                DATE_FORMAT: '%%Y-%%m-%%d',
                EXTENSION: '.md'
        }
        self.create_config_file(john_settings)

        self.assertFileExists(self.config_file)
        self.assertIncludeSettings(john_settings, self.config_file._data)

        # John runs oj
        self.app.run()

        # He sees that:
        #   * oj created note inside destination directory
        #   * notes name is todays date in ISO 8601 format with md extension
        #   * oj wrote John template text into note
        #   * note content is copy of his template file content
        file_name = '2012-12-21.md'
        destination = john_settings[DESTINATION].joinpath(file_name)

        self.assertEqual(destination, self.app.destination)
        self.assertEqual(destination.name, self.app.destination.name)

        template = self.template_file.data
        self.assertTemplateIsWrittenOnDestination(template)

        #   * oj opens note in editor that named in EDITOR env variable
        self.assertFileWasOpened(destination)


class OpenCreatedNoteTest(FunctionalTest):
    config_file_required      = True
    destination_file_required = True

    def test_run_with_existing_note_opens_it_without_overwriting_it(self):
        # John created new note with oj by his template
        template = self.template_file.data
        note = self.destination_file.data
        self.assertEqual(note, template)

        # He was being editing his new note when he accidentally closed it
        self.destination_file.replace_in_data(template, 'I am John and I')
        edited_note = self.destination_file.data
        self.assertIn('I am John and I', edited_note)
        self.assertNotEqual(edited_note, note)

        # John starts oj again and finds that his note is not overwritten
        self.app.run()
        note_after_new_run = self.destination_file.data

        self.mock_write_text.assert_not_called()
        self.assertEqual(note_after_new_run, edited_note)
        self.assertFileWasOpened(self.destination_file.path)


@patch('time.sleep')
class NoConfigTest(FunctionalTest):
    config_file_required   = False
    template_file_required = False

    def test_default_run_warns_user_and_gives_time_to_prevent_execution(
                self, mock_time_sleep
            ):
        # John migrated to another machine and brought his favourite app
        # with him (oj btw). Unfortenutely he forgot to create config file.
        # 
        # He runs oj and sees message that default settings will be used
        # Oj gives John enough time to read this message before main run
        default_wait_time = self.app.configurator.getint('DEFAULT', 'wait')
        self.assertGreaterEqual(default_wait_time, 3)

        # John does not want to run oj with default settings
        # He presses <c-c> to raise KeyboardInterrupt
        mock_time_sleep.side_effect = KeyboardInterrupt
        with self.assertRaise(KeyboardInterrupt):
            # with self.assertWarns(UserWarning): ?
            with warnings.catch_warnings(record=True) as w:
                self.app.run()

                self.assertEqual(len(w), 1)
                self.assertIsSubclass(w[-1].category, UserWarning)
                self.assertIn('Config file not found' in str(w[-1].message))
            mock_time_sleep.assert_called_once_with(default_wait_time)

    def test_run_without_any_configuration_uses_default_settings(
                self, mock_time_sleep
            ):
        # Jane has downloaded oj
        # She is a fun of trial and error learning
        # Because of that she runs oj to see that will happen

        # She sees message stating that the working directory will be 
        # used to store new notes. She is okay with it
        pwd = Path(__file__).parent.parent

        self.mock_getenv.side_effect = [pwd, 'vi']

        # with self.assertWarns(UserWarning): ?
        with warnings.catch_warnings(record=True) as w:
            self.app.run()
            self.assertEqual(len(w), 1)
            self.assertIsSubclass(w[-1].category, UserWarning)
            self.assertIn('Config file not found' in str(w[-1].message))

        # Oj runs after some wait and Jane sees that:
        #   * oj created note inside working directory
        #   * notes name is todays date in ISO 8601 format with txt extension
        #   * note is empty
        file_name = '2012-12-21.md'
        destination = pwd.joinpath(file_name)

        self.assertEqual(destination, self.app.destination)
        self.assertEqual(destination.name, self.app.destination.name)

        self.mock_write_text.assert_called_once_with('')
        self.assertEqual(destination.read_text(), 0)

        #   * oj opens note in editor that named in EDITOR env variable
        self.assertFileWasOpened(destination, 'EDITOR')


if __name__ == '__main__':
    main()

from datetime import date
from pathlib  import Path
from unittest import main
from unittest.mock import patch, MagicMock

from .base import FunctionalTest

from configurator import (DESTINATION, TEMPLATE, DATE_FORMAT, EXTENSION,
        HOLIDAY_TEMPLATE, HOLIDAY_FEATURE)


class CreateNewNote(FunctionalTest):
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


class HolidayNote(FunctionalTest):
    def test_expand_template_if_today_is_holiday(self):
        self.mock_date.today.return_value = MagicMock(spec=date, 
                **{'weekday.return_value': 5})  # today is a holiday
        # John likes to do week review of his live
        # He even created additional mini-template for this purpose
        # He wants to expand his daily template by this one for st and sn
        initial_template = self.template_file.data

        extra_path = self.config_file.path  # don't want to create another
        extra_template = f'{HOLIDAY_TEMPLATE}={str(extra_path)}'
        feature_on = f'{HOLIDAY_FEATURE}=1'
        args = [__file__, '-o', extra_template, feature_on]
        with patch('sys.argv', args):
            self.app.run()

        expanded_template = self.app.template

        self.assertNotEqual(initial_template, expanded_template)


if __name__ == '__main__':
    main()

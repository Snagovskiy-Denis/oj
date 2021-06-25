import os
import unittest
from pathlib import Path
from unittest import skip
from unittest.mock import patch

import test.base.fixtures as f
from constants import (DEFAULT_MODE, DESTINATION, TEMPLATE, 
        DATE_FORMAT)

from test.base.functional_test_class import FunctionalTest

from configurator import Configurator


class FirstRunTest(FunctionalTest):
    required_files = (f.TEMPLATE,)

    def test_run_with_valid_settings_creates_new_note(self):
        # John has downloaded oj
        # He wants to create new note by his template
        self.assertFileExists(f.TEMPLATE)

        # John checks documentation and finds that he needs config file 
        # TODO assert 'Required settings are:' in Configurator.__doc__
        # 
        # He runs touch {f.CONFIG} in the same directory as oj executable
        self.assertFileDoesNotExist(f.CONFIG)
        self.add_new_file(f.CONFIG)
        self.assertFileExists(f.CONFIG)

        # He writes to his new config file valid settings:
        #   * path to where create the note: {f.TEST_DIRECTORY}
        #   * path to his template file: {self.files[f.TEMPLATE].path}
        #   * {f.DATE_FORMAT} as desired filename format
        john_settings = {
                DESTINATION: f.TEST_DIRECTORY,
                TEMPLATE: self.files[f.TEMPLATE].path,
                DATE_FORMAT: f.DATE_FORMAT,
        }

        # John runs oj
        self.app.run()

        # He sees that:
        #   * oj creates note on DESTINATION path
        #   * notes name is formated todays date with {f.EXTENSION}
        #   * oj write his template text to note
        self.assertEqual(self.expected_path, self.app.destination)
        self.assertEqual(self.expected_path.name, self.app.destination.name)

        template = self.files[f.TEMPLATE].data
        self.assertTemplateIsWrittenOnDestination(template)

        #   * oj opens note in editor settled by {f.EDITOR} env variable
        self.assertFileWasOpened()


class OpenCreatedNoteTest(FunctionalTest):
    required_files = (f.TEMPLATE, f.CONFIG, f.DESTINATION)

    def test_run_with_existing_note_opens_it_without_overwriting_it(self):
        # John created new note with oj by his template
        template = self.files[f.TEMPLATE].data
        note = self.files[f.DESTINATION].data
        self.assertEqual(note, template)

        # He was being editing his new note when he accidentally closed it
        self.files[f.DESTINATION].replace_in_data(f.TEMPLATE, 'I am John a')
        edited_note = self.files[f.DESTINATION].data
        self.assertNotEqual(edited_note, note)

        # John starts oj again and finds that his note is not overwritten
        self.app.run()
        note_after_new_run = self.files[f.DESTINATION].data

        self.mock_write_text.assert_not_called()
        self.assertEqual(note_after_new_run, edited_note)
        self.assertFileWasOpened()


if __name__ == '__main__':
    unittest.main()

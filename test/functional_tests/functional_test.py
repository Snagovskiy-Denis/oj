import os
import unittest
from pathlib import Path
from unittest import skip
from unittest.mock import patch

import test.base.fixtures as f
from constants import (DEFAULT_MODE, DESTINATION, TEMPLATE, 
        DATE_FORMAT, TEST_DIRECTORY)

from test.base.functional_test_class import FunctionalTest

from configurator import Configurator


class FirstLaunchTest(FunctionalTest):
    required_files = (f.TEMPLATE,)

    def test_launch_with_valid_settings_creates_new_note(self):
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
        #   * path to where create the note: {TEST_DIRECTORY}
        #   * path to his template file: {self.files[f.TEMPLATE].path}
        #   * {f.DATE_FORMAT} as desired filename format
        john_settings = {
                DESTINATION: TEST_DIRECTORY,
                TEMPLATE: self.files[f.TEMPLATE].path,
                DATE_FORMAT: f.DATE_FORMAT,
        }

        # John runs oj
        # TODO self.app.run

        # He sees that:
        #   * oj creates note on DESTINATION path
        #   * notes name is formated todays date with {f.EXTENSION}
        self.app.read_config_file()    # TODO remove this
        self.app.build_filename()      # TODO remove this
        self.assertPathAndFilenameAreValid()

        #   * oj write his template text to note
        self.app.read_template_file()  # TODO remove this
        self.app.create_note()         # TODO remove this
        template = self.files[f.TEMPLATE].data
        self.assertTemplateIsWritten(template)

        #   * oj opens note in editor settled by ${f.EDITOR}
        self.app.open_note()           # TODO remove this
        self.assertFileWasOpened()


class FirstLaunchTestDeprecated(FunctionalTest):
    def test_launch_without_sys_args_with_default_settings_creates_new_note_(self):
        from warnings import warn
        warn(DeprecationWarning('Test does not tell *user* story'))
        # Script is being executed
        # There is only script pathname in system arguments
        # Because of that Script chooses default behaviour mode
        self.assertEqual(self.app.get_mode(), DEFAULT_MODE)

        # Secondly it checks if configuration file exist and reads it
        self.assertFileExists(f.CONFIG)

        self.app.read_config_file()
        settings = self.app.configurations

        # There are default settings values for:
        #   * destination path
        #   * template path
        #   * filenames' date format
        default_settings = {
                DESTINATION: TEST_DIRECTORY,
                TEMPLATE: self.files[f.TEMPLATE].path,
                DATE_FORMAT: f.DATE_FORMAT,
        }
        self.assertIncludeSettings(default_settings, settings)

        # It checks that default settings are valid and finds that:
        #   * files' name is todays date
        #   * date is formated by given date format
        self.app.build_filename()
        self.assertPathAndFilenameAreValid()

        #   * destination file does not exist yet
        self.assertFalse(self.app.destination.exists())

        #   * destination path is writable
        #   * template file on given path is readable
        self.assertPathsReadWriteAccessIsOK()

        self.app.read_template_file()
        template = self.app.template
        self.assertEqual(template, self.files[f.TEMPLATE].data)

        # It creates markdown file on destination path
        #   * files content identical to file on template path
        self.app.create_note()
        self.assertTemplateIsWritten(template)

        # It opens file in EDITOR (environment variable)
        #   * working directory changed to destination parent
        self.app.open_note()
        self.assertFileWasOpened()


if __name__ == '__main__':
    unittest.main()

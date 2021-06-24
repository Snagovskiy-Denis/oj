import os
import unittest
from pathlib import Path
from unittest.mock import patch

import test.base.fixtures as f
from constants import (DEFAULT_MODE, DESTINATION, TEMPLATE, 
        DATE_FORMAT, TEST_DIRECTORY)

from test.base.functional_test_class import FunctionalTest


class FirstLaunchTest(FunctionalTest):
    def test_launch_without_sys_args_with_default_settings_creates_new_note(
                                                                    self):
        pass

    # @unittest.skip
    def test_launch_without_sys_args_with_default_settings_creates_new_note_(
                                                                    self):
        # Script is being executed
        # TODO self.app.run()
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

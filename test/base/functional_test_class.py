import os
from unittest.mock import patch

import test.base.fixtures as f
from constants import TEST_DIRECTORY, EDITOR

from test.base.classes import IntegratedTestCase


class FunctionalTest(IntegratedTestCase):
    '''Create test environment and define new aseertion methods'''

    def assertFileExists(self, filename: str):
        self.assertTrue(self.files[filename].path.is_file())

    def assertFileDoesNotExist(self, filename: str):
        self.assertTrue(filename not in self.files.keys())

    def assertTemplateIsWrittenOnDestination(self, template):
        self.mock_write_text.assert_called_once_with(template)

    def assertFileWasOpened(self):
        self.mock_chdir.assert_called_once_with(self.expected_path.parent)
        self.mock_getenv.assert_called_once_with(EDITOR)
        self.mock_subprocess_run.assert_called_once_with(
            [self.mock_getenv.return_value, self.expected_path])

    def reset_open_note_related_mocks(self):
        self.mock_chdir.reset_mock()
        self.mock_getenv.reset_mock()
        self.mock_subprocess_run.reset_mock()

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
        with self.assertRaises(KeyError):
            self.assertFileExists(filename)

    def assertIncludeSettings(self, expected: dict, actual: dict):
        # self.assertDictEqual(expected | actual, expected)# output is ugly
        expected, actual = [set(s.items()) for s in (expected, actual)]
        try:
            assert expected <= actual
        except AssertionError as e:
            message = 'These settings: "{}" are not in the actual: {}'
            missing = dict(expected - actual)
            e.args += (message.format(missing, actual),)
            raise

    def assertPathAndFilenameAreValid(self):
        self.assertEqual(self.expected_path, self.app.destination)
        self.assertEqual(self.expected_path.name, self.app.destination.name)

    def assertTemplateIsWritten(self, template):
        self.mock_write_text.assert_called_once_with(template)

    def assertFileWasOpened(self):
        self.mock_chdir.assert_called_once_with(self.expected_path.parent)
        self.mock_getenv.assert_called_once_with(EDITOR)
        self.mock_subprocess_run.assert_called_once_with(
            [self.mock_getenv.return_value, self.expected_path])

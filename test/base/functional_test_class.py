import os
from unittest.mock import patch

import test.base.fixtures as f
from constants import TEST_DIRECTORY, EDITOR

from test.base.classes import IntegratedTestCase


class FunctionalTest(IntegratedTestCase):
    '''Create test environment and define new aseertion methods'''

    def assertPathsReadWriteAccessIsOK(self):
        self.assertFileExists(f.TEMPLATE)
        self.assertTrue(os.access(f.TEST_DIRECTORY, os.W_OK), 
            "Test have not write access to directory:\n{f.TEST_DIRECTORY}")
        self.assertTrue(os.access(self.files[f.TEMPLATE].path, os.R_OK),
            "Test have not read access on path:\n{f.TEST_DIRECTORY}")

    def assertFileExists(self, filename: str):
        self.assertTrue(self.files[filename].path.is_file())

    def assertIncludeSettings(self, expected: dict, actual: dict):
        # self.assertDictEqual(expected | actual, expected)  # this is too ugly
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
        self.mock_chdir.assert_called_once_with(self.expected_path)
        self.mock_getenv.assert_called_once_with(EDITOR)
        self.mock_subprocess_run.assert_called_once_with(
            [self.mock_getenv.return_value, self.expected_path])

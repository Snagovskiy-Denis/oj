from unittest import TestCase

from test.environment.full_environment import TestEnvironment

from oj import Application


class FunctionalTest(TestEnvironment, TestCase):
    '''Create test environment and define new aseertion methods'''

    def setUp(self):
        self.app = Application()
        self.initiate_test_environment()

    def tearDown(self):
        self.clear_test_environment()

    def assertFileExists(self, file):
        self.assertTrue(file.path.is_file())

    def assertFileDoesNotExist(self, path):
        self.assertFalse(path.is_file())

    def assertTemplateIsWrittenOnDestination(self, template):
        self.mock_write_text.assert_called_once_with(template)

    def assertIncludeSettings(self, expected, actual):
        if isinstance(expected, dict):
            expected = self.create_configurations(**expected)

        for section in expected.sections():
            for option in expected.options(section):
                actual_option = actual.get(section, option)
                expected_option = expected[section][option]
                self.assertEqual(expected_option, actual_option)

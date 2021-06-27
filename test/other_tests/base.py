from unittest import TestCase

from test.environment.fixture_files    import FixtureFiles
from test.environment.full_environment import TestEnvironment

from configurator import Configurator
from oj import Application


class ConfiguratorTestCase(FixtureFiles, TestCase):
    config_file_required   = True
    template_file_required = True

    def setUp(self):
        self.create_files()
        self.configurator = Configurator()

    def tearDown(self):
        self.delete_files()

    def assertIncludeSettings(self, expected, actual):
        for section in expected.sections():
            for option in expected.options(section):
                actual_option = actual.get(section, option)
                expected_option = expected[section][option]
                self.assertEqual(expected_option, actual_option)


class BaseApplicationTestCase(TestCase):
    def setUp(self):
        self.app = Application()


class IntegratedApplicationTestCase(TestEnvironment, TestCase):
    def setUp(self):
        self.app = Application()
        self.initiate_test_environment()

    def tearDown(self):
        self.clear_test_environment()


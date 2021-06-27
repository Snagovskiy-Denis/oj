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

    def assertIncludeSettings(self, expected: dict, actual: dict):
        # self.assertDictEqual(expected | actual, expected)  # output is ugly
        expected, actual = [set(s.items()) for s in (expected, actual)]
        try:
            assert expected <= actual
        except AssertionError as e:
            message = 'These settings: "{}" are not in the actual: {}'
            missing = dict(expected - actual)
            e.args += (message.format(missing, actual),)
            raise


class BaseApplicationTestCase(TestCase):
    def setUp(self):
        self.app = Application()


class IntegratedApplicationTestCase(TestEnvironment, TestCase):
    def setUp(self):
        self.app = Application()
        self.initiate_test_environment()

    def tearDown(self):
        self.clear_test_environment()


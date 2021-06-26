from test.base.classes import IntegratedTestCase

from constants import EDITOR


class FunctionalTest(IntegratedTestCase):
    '''Create test environment and define new aseertion methods'''

    def assertFileExists(self, file):
        self.assertTrue(file.path.is_file())

    def assertFileDoesNotExist(self, path):
        self.assertFalse(path.is_file())

    def assertTemplateIsWrittenOnDestination(self, template):
        self.mock_write_text.assert_called_once_with(template)

    def assertFileWasOpened(self, path):
        self.mock_chdir.assert_called_once_with(path.parent)
        self.mock_getenv.assert_called_once_with(EDITOR)
        self.mock_subprocess_run.assert_called_once_with(
            [self.mock_getenv.return_value, path])

    def assertConfigFileContains(self, settings: dict):
        for section_name, section in settings.items():
            self.assertIn(section_name, self.config_file.data,'Miss section')
            for setting_key, setting_value in section.items():
                self.assertIn(f'{setting_key} = {setting_value}', 
                                self.config_file.data,
                                'Miss settings')

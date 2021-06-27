from unittest.mock import patch

from .fixture_files import TEST_DIRECTORY

from constants import EDITOR


class FixtureSystem:
    '''Patchs system-depending input and prevent file-writing as output

    Patched enteties:

        * environment variables
        * system arguments
        * file writing
        * processes running
    '''
    def isolate_from_system(self):
        self.getenv_patcher = patch('oj.getenv', return_value='vi')
        self.sys_argv_patcher = patch('sys.argv', 
                [TEST_DIRECTORY.parent.joinpath('oj.py')])
        self.write_text_patcher = patch('pathlib.Path.write_text')
        self.subprocess_run_patcher = patch('subprocess.run')
        self.chdir_patcher = patch('oj.chdir')

        self.mock_getenv = self.getenv_patcher.start()
        self.sys_argv_mock = self.sys_argv_patcher.start()
        self.mock_write_text = self.write_text_patcher.start()
        self.mock_chdir = self.chdir_patcher.start() 
        self.mock_subprocess_run = self.subprocess_run_patcher.start()

    def stop_system_isolation(self):
        self.getenv_patcher.stop()
        self.sys_argv_patcher.stop()
        self.write_text_patcher.stop()
        self.chdir_patcher.stop() 
        self.subprocess_run_patcher.stop()

    def assertFileWasOpened(self, path):
        self.mock_chdir.assert_called_once_with(path.parent)
        self.mock_getenv.assert_called_once_with(EDITOR)
        self.mock_subprocess_run.assert_called_once_with(
            [self.mock_getenv.return_value, path])

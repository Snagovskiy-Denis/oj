from unittest import main
from unittest.mock import patch
from pathlib  import Path

from .base import FunctionalTest

from configurator import DESTINATION, DATE_FORMAT
from oj import Application


class SkipWarningMessage(FunctionalTest):
    config_file_required      = False
    template_file_required    = False
    destination_file_required = False

    def setUp(self):
        super().setUp()
        self.config_path_patcher.stop()

        self.is_file_patcher = patch('pathlib.Path.is_file', 
                return_value=False)
        self.sleep_patcher = patch('time.sleep') 

        self.mock_is_file = self.is_file_patcher.start()
        self.mock_sleep = self.sleep_patcher.start()

    def tearDown(self):
        self.is_file_patcher.stop()
        self.sleep_patcher.stop()

    def assertNoWarnsRun(self, isolate=True):
        try:
            with self.assertWarns(UserWarning):
                if isolate:
                    Application().run()
                else:
                    self.app.run()
        except AssertionError:
            pass  # should not raise
        else:
            self.fail('Warning message is not skipped')

    def test_skip_warning_message(self):
        # Jane uses oj with defaults awhile
        # She has tired of default warning message
        with self.assertWarns(UserWarning) as w:
            with patch('configparser.ConfigParser.read'):
                Application().run()

        # In the warning message she sees hint of how to skip it
        self.assertIn('--skip', str(w.warnings[-1].message))

        # Jane alias oj to oj --skip and after that message is gone for good
        with patch('sys.argv', [__file__, '--skip']):
            self.assertNoWarnsRun()

    def test_overwrite_multiple_options_on_run(self):
        # Jane does not want to pollute .config directory with one more config
        # But she does not happy with default settings either
        # She discover that she can set destination directory without ini file
        # 
        # Jane runs oj with overwrite argument to change:
        #     * destination path
        #     * date format
        destination = f'{DESTINATION}=~/Data/notes'
        date_format = f"'{DATE_FORMAT} = %%d.%%m.%%Y'"
        args = [__file__, '--skip', '-o', destination, date_format]
        with patch('sys.argv', args):
            self.assertNoWarnsRun(isolate=False)

        # self.assertIsInstance(self.app.cli.option, dict)
        # self.assertEqual(self.app.cli.option[DATE_FORMAT], '%%d.%%m.%%Y')
        # self.assertEqual(self.app.cli.option[DESTINATION], '~/Data/notes')

        self.assertEqual(
                self.app.configurator.get_path(DESTINATION),
                Path().home().joinpath('Data', 'notes')
        )
        self.assertEqual(
                self.app.configurator.get_in_filename(DATE_FORMAT),
                '%d.%m.%Y'
        )


if __name__ == '__main__':
    main()

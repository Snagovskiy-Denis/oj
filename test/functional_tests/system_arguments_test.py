from unittest import main
from unittest.mock import patch
from pathlib  import Path

from .base import FunctionalTest

from oj import Application


@patch('time.sleep')
@patch('pathlib.Path.is_file', return_value=False)
class SkipWarningMessage(FunctionalTest):
    config_file_required      = False
    template_file_required    = False
    destination_file_required = False

    def setUp(self):
        super().setUp()
        self.config_path_patcher.stop()

    def test_skip_warning_message(self, mock_is_file, mock_sleep):
        # Jane uses oj with defaults awhile
        # She has tired of default warning message
        with self.assertWarns(UserWarning) as w:
            with patch('configparser.ConfigParser.read'):
                self.app.run()

        # In the warning message she sees hint of how to skip it
        self.assertIn('--skip', str(w.warnings[-1].message))

        # Jane alias oj to oj --skip and after that message is gone for good
        try:
            with patch('sys.argv', [__file__, '--skip']):
                with self.assertWarns(UserWarning) as w2:
                    Application().run()
        except AssertionError:
            pass  # should not raise
        else:
            self.fail('Warning message is not skipped')


class RewriteArgumentTest(FunctionalTest):
    config_file_required      = False
    template_file_required    = False
    destination_file_required = True

    def test_(self):
        pass


if __name__ == '__main__':
    main()

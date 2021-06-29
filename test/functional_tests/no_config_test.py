from pathlib import Path
from unittest import main
from unittest.mock import patch

from .base import FunctionalTest


@patch('time.sleep')
@patch('pathlib.Path.is_file', return_value=False)
class NoConfigTest(FunctionalTest):
    config_file_required   = False
    template_file_required = False

    def setUp(self):
        super().setUp()
        self.config_path_patcher.stop()

    def assertIsDefaultsWarningMessage(self, w):
        self.assertEqual(len(w.warnings), 1)
        warning_message = str(w.warnings[-1].message)
        self.assertIn('Defaults will be used', warning_message)
        self.assertIn('if you do not want default run', warning_message)
        self.assertIn('to skip this message next time', warning_message)

    def test_default_run_warns_user_and_gives_time_to_prevent_execution(
                self, mock_is_file, mock_time_sleep
            ):
        # John migrated to another machine and brought his favourite app
        # with him (oj btw). Unfortenutely he forgot to create config file.
        # 
        # He runs oj and sees message that default settings will be used
        # Oj gives John enough time to read this message before main run
        default_wait_time = self.app.configurator.getint('DEFAULT', 'wait')
        self.assertGreaterEqual(default_wait_time, 5)

        # John does not want to run oj with default settings
        # He presses <c-c> to raise KeyboardInterrupt
        mock_time_sleep.side_effect = KeyboardInterrupt
        with self.assertRaises(KeyboardInterrupt):
            with self.assertWarns(UserWarning) as w:
                self.app.run()

        mock_time_sleep.assert_called_once_with(default_wait_time)

        self.assertIsDefaultsWarningMessage(w)

    def test_run_without_any_configuration_uses_default_settings(
                self, mock_is_file, mock_time_sleep
            ):
        # Jane has downloaded oj
        # She is a fun of trial and error learning
        # Because of that she runs oj to see that will happen

        # She sees message stating that the working directory will be 
        # used to store new notes. She is okay with it
        with self.assertWarns(UserWarning) as w:
            with patch('configparser.ConfigParser.read'):
                self.app.run()

        self.assertIsDefaultsWarningMessage(w)

        # Oj runs after some wait and Jane sees that:
        #   * oj created note inside working directory
        #   * notes name is todays date in ISO 8601 format with txt extension
        #   * note is empty
        file_name = '2012-12-21.txt'
        destination = Path().absolute().joinpath(file_name)

        self.assertEqual(destination, self.app.destination)
        self.assertEqual(destination.name, self.app.destination.name)

        self.mock_write_text.assert_called_once_with('')

        #   * oj opens note in editor that named in EDITOR env variable
        self.assertFileWasOpened(destination, 'EDITOR')


if __name__ == '__main__':
    main()

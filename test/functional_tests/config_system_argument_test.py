from pathlib  import Path
from unittest import main
from unittest.mock import patch
import io

from .base import FunctionalTest

from configurator import Configurator


class OpenConfigFile(FunctionalTest):
    def test_open_config_file_if_config_file_exist(self):
        # John wants to see his config file
        # In order to do so he runs oj with --config argument
        self.assertFileExists(self.config_file)

        with patch('sys.argv', [__file__, '--config']):
            self.app.run()

        # John sees that oj opened his config file
        self.assertFileWasOpened(self.config_file.path)


class CreateConfigFile(FunctionalTest):
    config_file_required = False

    def setUp(self):
        super().setUp()
        self.config_path_patcher.stop()

    def test_writes_new_config_file_if_it_does_not_exist(self):
        # Jane is decided that it is worth to config file for oj now
        # She runs oj with --config argument and sees prompt line
        # It says that it will be created new file on path ~/.config/oj.ini
        # She accept the prompt with joyful feeling of ojs user-friendliness
        config_path = self.app.configurator._get_config_path(skip=True)
        with patch('sys.argv', [__file__, '--skip', '--config']):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                with patch('builtins.input', return_value='y') as mock_input:
                    with patch('pathlib.Path.is_file', return_value=False):
                        with patch('pathlib.Path.exists', return_value=False):
                            self.app.run()
        self.assertIn('/.config/oj.ini', mock_stdout.getvalue())
        mock_input.assert_called_once()

        # She sees that oj created and opened config file on prompted path
        self.assertEqual(self.app.destination, config_path)
        default_config_text = Configurator().get_default_config()
        self.mock_write_text.assert_called_once_with(default_config_text)

        self.assertFileWasOpened(config_path)


if __name__ == '__main__':
    main()

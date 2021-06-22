import pathlib
import sys
from configparser import ConfigParser


PROJECT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
CONFIG_FILENAME = 'config.md'  # TODO config.ini


class ConfigReadError(Exception):
    'Config file is readeble but its properties corrupted'

    def __init__(self, *arguments, message='Can not read {}: "{}"'):
        message = message.format(*arguments)
        super().__init__(message)

class SectionReadError(ConfigReadError):
    def __init__(self, section_name):
        super().__init__('section', section_name)

class SettingReadError(ConfigReadError):
    def __init__(self, setting_name):
        super().__init__('setting', setting_name)


class Configurator:
    PATH_SETTINGS = ('destination', 'template')
    FILENAME_SETTINGS = ('date format',)
    ALL_SETTINGS = PATH_SETTINGS, FILENAME_SETTINGS

    def __init__(self):
        self.config = ConfigParser()

    def read_config(self):
        configurations = dict()
        self.config.read(self._get_config_path())

        sections = self.config.sections()
        if not sections:
            raise ValueError('Config file is empty')

        for section, section_settings in zip(sections, self.ALL_SETTINGS):
            if not self.config.has_section(section):
                raise SectionReadError(section)

            for setting in section_settings:
                if not self.config.get(section, setting, fallback=None):
                    raise SettingReadError(setting)

                value = self.config[section][setting]
                if setting in self.PATH_SETTINGS:
                    value = pathlib.Path(value)
                configurations[setting] = value
        return configurations

    def _get_config_path(self):
        path = pathlib.Path(__file__).parent.joinpath(CONFIG_FILENAME)
        if not path.is_file():
            raise FileNotFoundError('Config file not found on path:\n\n' \
                    f'{path=}')
        return str(path)
    

class Application:
    DEFAULT = 'DEFAULT'

    def __init__(self):
        self.path = pathlib.Path().absolute()

    def get_mode(self):
        return self.DEFAULT

    def read_config_file(self):
        return Configurator().read_config()


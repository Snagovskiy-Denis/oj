from configparser import ConfigParser
from pathlib import Path

from constants import (PATH_SETTINGS, FILENAME_SETTINGS, ALL_SETTINGS, 
        CONFIG_FILENAME, BASE_DIRECTORY)
from exceptions import SectionReadError, SettingReadError


class Configurator:
    '''Read, resolve and write configurations

    Sections:

        * DEFAULT  -- this settings is used unless another section overwrite it
        * PATH     -- paths to required and optional files (e.g. for note creation)
        * FILENAME -- rules for build destination path filenames part 

    PATH:

        * 
    '''

    def __init__(self):
        self.config = ConfigParser()

    def read_config(self) -> dict():
        configurations = dict()
        self.config.read(self._get_config_path())

        sections = self.config.sections()
        if not sections:
            raise ValueError('Config file is empty')

        for section, section_settings in zip(sections, ALL_SETTINGS):
            if not self.config.has_section(section):
                raise SectionReadError(section)

            for setting in section_settings:
                if not self.config.get(section, setting, fallback=None):
                    raise SettingReadError(setting)

                value = self.config[section][setting]
                if setting in PATH_SETTINGS:
                    value = Path(value)
                configurations[setting] = value
        return configurations

    def _get_config_path(self):
        path = BASE_DIRECTORY.joinpath(CONFIG_FILENAME)
        if not path.is_file():
            raise FileNotFoundError('Config file not found on path:\n\n' \
                    f'{path=}')
        return str(path)

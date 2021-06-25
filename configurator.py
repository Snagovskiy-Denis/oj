from configparser import ConfigParser
from pathlib import Path

from constants import (PATH_SETTINGS, FILENAME_SETTINGS, ALL_SETTINGS, 
        CONFIG_PATH)
from exceptions import SectionReadError, SettingReadError


class Configurator:
    '''Read, resolve and write configurations

    Sections:

        * DEFAULT  -- uses these settings unless another section overwrite it
        * PATH     -- absolute paths to files
        * FILENAME -- rules for build destination path filenames part 


    Settings:

        PATH:

            * destination - directory where notes are located
            * template    - use this file text data as base to new note

        FILENAME:

            * date format - note filename is todays
            * extension   - end-part of new note filename


    Config file example:

        [PATH]
        destination = /home/John_Doe/notes
        template    = /home/John_Doe/notes/new_note_template.md

        [FILENAME]
        # ISO 8601 format
        # All valid formats: https://docs.python.org/library/datetime
        date format = %%Y-%%m-%%d
        extension   = .md
    '''

    def __init__(self):
        # class Configuratori(ConfigParser) ?
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
        path = CONFIG_PATH
        if not path.is_file():
            raise FileNotFoundError('Config file not found on path:\n\n' \
                    f'{path=}')
        return str(path)

from configparser import ConfigParser, NoSectionError
from pathlib import Path

from constants import (PATH_SETTINGS, FILENAME_SETTINGS, ALL_SETTINGS, 
        APPLICATION_NAME, FILENAME_SECTION, PATH_SECTION)
from exceptions import SectionReadError, SettingReadError


class Configurator(ConfigParser):
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
    # TODO move settings hierarchy to this file

    def __init__(self):
        # ConfigParser __init__ defaults attr does not work so...
        super().__init__()
        self._set_defaults()

    def getpath(self, option, section=PATH_SECTION) -> Path:
        option = self.get(section, option)
        return Path(option).absolute()

    def read(self) -> dict():
        super().read(self._get_config_path())
        if not self.sections():
            raise ValueError('Config file is empty')
        return self

    def _set_defaults(self):
        # TODO: dict_read
        # defaults:
        #     * date format = %%Y-%%m-%%d
        #     * extension   = .md
        #     * config path = {path to .config plus 'oj.ini'}
        #     * destination = {$PWD env var}
        #     * template    = ''
        #
        #     [OPEN]
        #     * use EDITOR  = {boolean}
        #     * use VISUAL  = {boolean}
        #     * 
        #     * editor name = # will be used if EDITOR and VISUAL are false
        #     * 
        # 
        pass

    def _get_config_path(self):
        file_name = f'{APPLICATION_NAME}.ini'
        path = Path().home().joinpath('.config', file_name)
        if not path.is_file():
            # TODO warnings.warn(UserWarning('Defaults will be used...'))
            # time.sleep(3)
            # do not raise
            # Disable this warning if valid sys argument provided
            raise FileNotFoundError('Config file not found on path:\n\n' \
                    f'{path=}')
        return path

from configparser import ConfigParser, NoSectionError
from pathlib import Path


APPLICATION_NAME = 'oj'

DEFAULT_SECTION  = 'DEFAULT'
PATH_SECTION     = 'PATH'
FILENAME_SECTION = 'FILENAME'

PATH_OPTIONS     = DESTINATION, TEMPLATE  = 'destination', 'template'
FILENAME_OPTIONS = DATE_FORMAT, EXTENSION = 'date_format', 'extension'


class Configurator(ConfigParser):
    '''Read, resolve and write configurations

    Sections:

        * PATH     -- absolute paths to files
        * FILENAME -- rules for build destination path filenames part 

    Settings:

        PATH:

            * destination - directory where notes are located
            * template    - use this file text data as base to new note

        FILENAME:

            * date_format - note filename is todays
            * extension   - end-part of new note filename


    Config file example:

        [PATH]
        destination = /home/John_Doe/notes
        template    = /home/John_Doe/notes/new_note_template.md

        [FILENAME]
        # ISO 8601 format
        # All valid formats: https://docs.python.org/library/datetime
        date_format = %%Y-%%m-%%d
        extension   = .md
    '''
    def __init__(self, options = dict(), set_defaults = True):
        # ConfigParser __init__ defaults attr does not work so...
        super().__init__()
        self._set_defaults()
        # if set_defaults:
        #     self._set_defaults()
        # if options:
        #     self.read_dict(options)

    def get_path(self, option: str, section=PATH_SECTION) -> Path:
        '''Get option as instance of Path class'''
        option = self.get(section, option)
        return Path(option).absolute()
    
    def get_in_filename(self, option: str) -> str:
        '''Shortcut for getting option from filename section'''
        return self.get(FILENAME_SECTION, option)

    def read(self) -> dict():
        super().read(self._get_config_path())
        if not self.sections():
            raise ValueError('Config file is empty')
        return self

    def _set_defaults(self):
        # TODO: dict_read
        # defaults:
        #     * date_format = %%Y-%%m-%%d
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
        '''Validate config file path'''
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
    
    def __str__(self):
        return str(self._sections)

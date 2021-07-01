from configparser import ConfigParser
from pathlib import Path
import time
import warnings


APPLICATION_NAME = 'oj'

PATH_SECTION     = 'PATH'
DEFAULT_SECTION  = 'DEFAULT'
FILENAME_SECTION = 'FILENAME'
STAFF_ONLY       = 'STAFF_ONLY'

DESTINATION, TEMPLATE, HOLIDAY_TEMPLATE = 'destination', 'template', 'holiday'
WAIT = 'wait'
HOLIDAY_FEATURE = 'holiday_feature'
DATE_FORMAT, EXTENSION = 'date_format', 'extension'
CONFIG_DIRECTORY = 'config_directory'
USE_EDITOR, USE_VISUAL = '1', '0'


#     [OPEN]
#     * use EDITOR  = {boolean}
#     * use VISUAL  = {boolean}
#     * 
#     * editor name = # will be used if EDITOR and VISUAL are false
DEFAULTS = {

              STAFF_ONLY: {

                           WAIT: '7',
                HOLIDAY_FEATURE: '0',

        },

            PATH_SECTION: {

                    DESTINATION: '',
                       TEMPLATE: '',
               CONFIG_DIRECTORY: f'{Path().home().joinpath(".config")}',
               HOLIDAY_TEMPLATE: ''

        },

        FILENAME_SECTION: {

                    DATE_FORMAT: '%%Y-%%m-%%d',
                      EXTENSION: '.txt',

        },
}


class Configurator(ConfigParser):
    '''Read, resolve and write configurations

    Sections:

        * PATH     -- absolute paths to files
        * FILENAME -- rules for build destination path filenames part 

    Settings:

        PATH:

                 destination  -- directory where notes are located

                     template -- use this file text data as base to new note

             config_directory -- search oj.ini file in this directory
                                 for --option system argument usage
                                 should not be placed in oj.ini file itself

        FILENAME:

                   date_format -- note filename is todays

                     extension -- end-part of new note filename


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
        super().__init__()
        if set_defaults: self.read_dict(DEFAULTS)

    def get_path(self, option: str, section=PATH_SECTION) -> Path:
        '''Get option as instance of Path class'''
        option = self.get(section, option)
        return Path(option).expanduser().absolute()
    
    def get_in_filename(self, option: str) -> str:
        '''Shortcut for getting option from filename section'''
        return self.get(FILENAME_SECTION, option)

    def read(self, cli_options=None, skip=False) -> dict():
        super().read(self._get_config_path(skip))
        if cli_options is not None:
            self.read_additional_options(cli_options)
        return self

    def read_additional_options(self, cli_options: dict):
        'Find section which given option belongs to and overwrite its value'
        for section in self.sections():
            for key, value in cli_options.items():
                if key in self[section].keys():
                    self[section][key] = value

    def _get_config_path(self, skip=False):
        '''Validate config file path'''
        file_name = f'{APPLICATION_NAME}.ini'
        path = self.get_path(CONFIG_DIRECTORY).joinpath(file_name)
        if not path.is_file() and not skip:
            path = ''

            message = f'''



            Config had not been found. Defaults will be used.

            Press <Ctrl+C> if you do not want default run.
            If you do then just wait.

            Use --skip flag option to skip this message next time

            '''
            warnings.warn(UserWarning(message))

            wait_time = self.getint('STAFF_ONLY', 'wait')
            time.sleep(wait_time)
        return path
    
    def get_default_config(self):
        '''Default config file writable body'''
        return '\n'.join(
         (f'[{PATH_SECTION}]',
           '# Tilde symbol (~) in path section will be expanded to user home',
           '#',
           '# Destination is the directory where notes will be located',
           '# e.g. destination = ~/notes',
           "destination = ''",
           '',
           '# Point on template file',
           '# New note will be copy of templates file',
           '# e.g. template = ~/notes/new_note_template.md',
           "template = ''",
           '',
          f'[{FILENAME_SECTION}]',
           '# Date format is used to format notes name. ISO 8601 is default.',
           '# Could include any symbols but % starts python datetime format',
           '# Double % (%%) is used to escape single % in .ini files',
           '# All valid formats: https://docs.python.org/library/datetime',
           'date_format = %%Y-%%m-%%d',
           '',
           "# 'Extension' is part of the notes name after date_format",
           'extension = .txt',
         )
       )

    def __str__(self):
        return str(self._sections)

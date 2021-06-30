from pathlib import Path
from datetime import date
from unittest.mock import patch, Mock

from configurator import Configurator
from configurator import (PATH_SECTION, FILENAME_SECTION, DEFAULT_SECTION,
        DATE_FORMAT, EXTENSION, DESTINATION, TEMPLATE, 
        HOLIDAY_FEATURE, HOLIDAY_TEMPLATE )


# Default test data
TEST_DIRECTORY = Path(__file__).parent.parent

FAKE_DATE = date(2012, 12, 21)

TEST_CONFIG_FILENAME      = 'config'
TEST_TEMPLATE_FILENAME    = 'template'
TEST_DESTINATION_FILENAME = FAKE_DATE.isoformat() + '.md'

TEST_CONFIG_PATH          = TEST_DIRECTORY.joinpath(TEST_CONFIG_FILENAME)
TEST_TEMPLATE_PATH        = TEST_DIRECTORY.joinpath(TEST_TEMPLATE_FILENAME)
TEST_DESTINATION_PATH     = TEST_DIRECTORY

TEST_CONFIG_DATA = {
                 EXTENSION: '.md',
               DATE_FORMAT: '%%Y-%%m-%%d', 
               DESTINATION: TEST_DESTINATION_PATH,
                  TEMPLATE: TEST_TEMPLATE_PATH,
}
TEST_TEMPLATE_DATA = f'''# Dear diary
## Todays Evil scheming 
{TEST_TEMPLATE_FILENAME}

- [x] write tests for life
- [ ] live a life
- [ ] refactor life
'''
TEST_DESTINATION_DATA = TEST_TEMPLATE_DATA


class SelfCleaningTestFile:
    '''Creates and deletes file on path with given plaintext data'''

    def __init__(self, file_name: str, data: str):
        self._path = TEST_DIRECTORY.joinpath(file_name)
        self._data = data
        self._write_file()

    def _write_file(self, rewrite: bool = False):
        if rewrite or not self._path.is_file():
            # Path.write_text might be patched so could not be used
            with open(self._path, 'w') as f:  
                f.write(self._data)

    def replace_in_data(self, old: str, new: str):
        self._data = self._data.replace(old, new)
        self._write_file(rewrite=True)

    @property
    def path(self) -> Path:
        return self._path

    @property
    def data(self) -> str:
        return str(self._data)

    def __repr__(self):
        return f'{self.path.name=}'

    def __del__(self):
        if self._path.is_file():
            self._path.unlink()


class PlainTextTestFile(SelfCleaningTestFile):
    '''Creates and deletes file on path with given plaintext data'''


class ConfigTestFile(SelfCleaningTestFile):
    '''Creates and deletes file on path with given Configurator data'''

    def __init__(self, file_name: str, data: Configurator):
        super().__init__(file_name, data)

    def _write_file(self, rewrite: bool = False):
        if rewrite or not self._path.is_file():
            with open(self._path, 'w') as f:
                self._data.write(f)

    def replace_in_data(self, old: str, new: str):
        for section in self._data.sections():
            for key, value in self._data.items(section):
                if old == value:
                    self._data[section][key] = new
        self._write_file(rewrite=True)


class FixtureFiles:
    '''Create and delete test files; patch Configurator path and todays date'''

    config_file_required      = False
    template_file_required    = False
    destination_file_required = False

    date_format = '%Y-%m-%d'

    def create_files(self):
        self._patch_config_path()
        self._patch_date()


        self.files = dict[str: 'file name', SelfCleaningTestFile]()
        if self.template_file_required: 
            self.create_template_file()
        if self.destination_file_required:
            self.create_destination_file(self.date_format)
        if self.config_file_required: 
            config_data = self.create_configurations(**TEST_CONFIG_DATA)
            self.create_config_file(data=config_data)

    def create_configurations(self, date_format='%%Y-%%m-%%d', 
            extension='.md', destination=None, template=None, 
            holiday_on=None, holiday_path=None):
        '''Get configurations without reading config file'''
        # Integrate configurator.defaults here...
        d  = destination if destination is not None else TEST_DESTINATION_PATH
        t  = template    if template    is not None else TEST_TEMPLATE_PATH
        h  = '1'         if holiday_on  is not None else '0'
        ht = TEST_CONFIG_PATH if holiday_path       else ''
        configurator = Configurator()
        configurator.read_dict({

                'STAFF_ONLY': {
                                HOLIDAY_FEATURE: h
                              },

            FILENAME_SECTION: {
                                DATE_FORMAT: date_format,
                                EXTENSION: extension,
                              },

            PATH_SECTION:     {
                                TEMPLATE: t,
                                DESTINATION: d,
                                HOLIDAY_TEMPLATE: ht,
                              },
        })
        return configurator

    def create_config_file(self, data: Configurator = None):
        if not data:
            data = self.create_configurations()
        elif isinstance(data, dict):
            data = self.create_configurations(**data)
        self.files[TEST_CONFIG_FILENAME] = ConfigTestFile(
                TEST_CONFIG_FILENAME, data)

    def create_template_file(self, file_data: str = TEST_TEMPLATE_DATA):
        self.files[TEST_TEMPLATE_FILENAME]= PlainTextTestFile(
                TEST_TEMPLATE_FILENAME, file_data)

    def create_destination_file(self, date_format='%Y-%m-%d', extension='.md'):
        new_filename = FAKE_DATE.strftime(date_format) + extension
        self.files[TEST_DESTINATION_FILENAME] = PlainTextTestFile(
            new_filename, TEST_DESTINATION_DATA)

    @property
    def destination_directory(self) -> Path:
        return TEST_DIRECTORY

    @property
    def template_file(self) -> PlainTextTestFile:
        return self.files[TEST_TEMPLATE_FILENAME]

    @property
    def config_file(self) -> ConfigTestFile:
        return self.files[TEST_CONFIG_FILENAME]

    @property
    def destination_file(self) -> PlainTextTestFile:
        return self.files[TEST_DESTINATION_FILENAME]
    
    def _patch_date(self):
        config = {'today.return_value': FAKE_DATE, 'weekday.return_value': 5}
        self.date_patcher = patch('oj.date', **config)
        self.mock_date = self.date_patcher.start()

    def _patch_config_path(self):
        '''Search config file on given path only and do not validate path'''
        self.config_path_patcher = patch(
                'configurator.Configurator._get_config_path', 
                return_value = TEST_CONFIG_PATH
        )
        self.mock_config_path = self.config_path_patcher.start()

    def delete_file(self, file: SelfCleaningTestFile):
        del self.files[file.path.name]

    def delete_files(self):
        self.date_patcher.stop()
        self.config_path_patcher.stop()

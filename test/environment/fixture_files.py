from pathlib import Path
from datetime import date
from unittest.mock import patch

from constants import (DEFAULT_SECTION, PATH_SECTION, FILENAME_SECTION,
        DATE_FORMAT, EXTENSION, DESTINATION, TEMPLATE)


# Default test data
TEST_DIRECTORY = Path(__file__).parent.parent.parent.joinpath('test')

FAKE_DATE = date(2012, 12, 21)

TEST_CONFIG_FILENAME      = 'config'
TEST_TEMPLATE_FILENAME    = 'template'
TEST_DESTINATION_FILENAME = FAKE_DATE.isoformat() + '.md'

TEST_TEMPLATE_DATA = f'''# Dear diary
## Todays Evil scheming 
{TEST_TEMPLATE_FILENAME}

- [x] write tests for life
- [ ] live a life
- [ ] refactor life
'''
TEST_CONFIG_DATA = f'''[{DEFAULT_SECTION}]
{DATE_FORMAT} = %%Y-%%m-%%d
{EXTENSION} = .md

[{PATH_SECTION}]
{DESTINATION} = {TEST_DIRECTORY.joinpath(TEST_DESTINATION_FILENAME).parent}
{TEMPLATE} = {TEST_DIRECTORY.joinpath(TEST_TEMPLATE_FILENAME)}

[{FILENAME_SECTION}]
'''
TEST_DESTINATION_DATA = TEST_TEMPLATE_DATA

TEST_CONFIG      = TEST_CONFIG_FILENAME, TEST_CONFIG_DATA
TEST_TEMPLATE    = TEST_TEMPLATE_FILENAME, TEST_TEMPLATE_DATA
TEST_DESTINATION = TEST_DESTINATION_FILENAME, TEST_DESTINATION_DATA

TEST_FILES = TEST_CONFIG, TEST_TEMPLATE, TEST_DESTINATION


class SelfCleaningTestFile:
    'Create and delete file on path with given data'

    def __init__(self, file_name: str, data:str=''):
        self._path = TEST_DIRECTORY.joinpath(file_name)
        self._data = data
        self._write_file()

    def _write_file(self, rewrite: bool = False):
        if rewrite or not self._path.is_file():
            # Path.write_text might be patched
            with open(self._path, 'w') as f:  
                f.write(self._data)

    @property
    def path(self) -> Path:
        return self._path

    @property
    def data(self) -> str:
        return self._data

    def replace_in_data(self, old, new):
        self._data = self._data.replace(old, new)
        self._write_file(rewrite=True)

    def __repr__(self):
        return f'{self.path.name=}'

    def __del__(self):
        if self._path.is_file():
            self._path.unlink()


class FixtureFiles:
    '''Create and delete files. Patch config path and todays date'''
    config_file_required      = False
    template_file_required    = False
    destination_file_required = False
    date_format = '%Y-%m-%d'

    def create_files(self):
        self.files = dict[str: 'file name', SelfCleaningTestFile]()

        for file_name, file_data in TEST_FILES:
            self.files[file_name] = self.add_new_file(file_name, file_data)
        if self.date_format != '%Y-%m-%d':
            self.create_destination_file(date_format)

        self._patch_config_path()
        self._patch_date()

        if not self.config_file_required: self.delete_file(self.config_file)
        if not self.template_file_required: 
            self.delete_file(self.template_file)
        if not self.destination_file_required: 
            self.delete_file(self.destination_file)

    def create_configurations(self, date_format='%Y-%m-%d', extension='.md', 
            destination=None, template=None):
        '''Get configurations without reading config file'''
        dest = destination if destination else self.destination_directory 
        template = template if template else self.template_file.path
        return {DATE_FORMAT: date_format, EXTENSION: extension,
                DESTINATION: dest, TEMPLATE: template}

    def add_new_file(self, file_name, file_data) -> SelfCleaningTestFile:
        return SelfCleaningTestFile(file_name, file_data)
    
    def delete_file(self, file: SelfCleaningTestFile):
        del self.files[file.path.name]

    def create_config_file(self, new_settings: dict = TEST_CONFIG_DATA):
        all_settings = []
        for section_name, section in new_settings.items():
            all_settings.append(f'[{section_name}]')
            settings = [f'{key} = {value}' for key, value in section.items()]
            all_settings += settings
        self.files[TEST_CONFIG_FILENAME] = self.add_new_file(
                TEST_CONFIG_FILENAME, '\n'.join(all_settings))

    def create_template_file(self, file_data: str = TEST_TEMPLATE_DATA):
        self.files[TEST_TEMPLATE_FILENAME]= self.add_new_file(
                TEST_TEMPLATE_FILENAME, file_data)

    def create_destination_file(self, date_format='%Y-%m-%d'):
        new_filename = FAKE_DATE.strformat(self.date_format) + '.md'
        self.files[TEST_DESTINATION_FILENAME] = SelfCleaningTestFile(
            new_filename, TEST_DESTINATION_DATA)

    @property
    def destination_directory(self) -> Path:
        return TEST_DIRECTORY

    @property
    def template_file(self) -> SelfCleaningTestFile:
        return self.files[TEST_TEMPLATE_FILENAME]

    @property
    def config_file(self) -> SelfCleaningTestFile:
        return self.files[TEST_CONFIG_FILENAME]

    @property
    def destination_file(self) -> SelfCleaningTestFile:
        return self.files[TEST_DESTINATION_FILENAME]
    
    def _patch_date(self):
        self.date_patcher = patch('oj.date', 
                **{'today.return_value': FAKE_DATE})
        self.mock_date = self.date_patcher.start()

    def _patch_config_path(self):
        self.config_path_patcher = patch(
                'configurator.Configurator._get_config_path', 
                return_value=self.files[TEST_CONFIG_FILENAME].path)
        self.mock_config_path = self.config_path_patcher.start()

    def delete_files(self):
        self.date_patcher.stop()
        self.config_path_patcher.stop()

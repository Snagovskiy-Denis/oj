from pathlib import Path

from unittest.mock import patch

import test.base.fixtures as f
from constants import (DEFAULT_SECTION, PATH_SECTION, FILENAME_SECTION,
                       DESTINATION, TEMPLATE, DATE_FORMAT, EXTENSION,
                       TEST_DIRECTORY,
                      )


class SelfCleanedFile:
    'Create and delete file on path with given data'

    def __init__(self, path:Path, data:str=''):
        self._path = path
        self._data = data
        self._write_file()

    def _write_file(self):
        if not self._path.is_file():
            # Path.write_text might be patched
            with open(self._path, 'w') as f:  
                f.write(self._data)

    @property
    def path(self):
        return self._path

    @property
    def data(self):
        return self._data

    def replace_in_data(self, old, new):
        self._data = self._data.replace(old, new)
        self._write_file()

    def __repr__(self):
        return f'{self.path.name=}'

    def __del__(self):
        if self._path.is_file():
            self._path.unlink()


class SelfCleanedFileFactory:
    def __init__(self, desired_files: tuple[str: 'filename']):
        self.desired_files = desired_files

    def produce(self) -> dict[str: 'filename', SelfCleanedFile]:
        datas = self.generate_files_data()
        paths = self.generate_filepaths()

        files = dict()
        for file in self.desired_files:
            _data = {'path': paths[file], 'data': datas.get(file, '')}
            files[file] = SelfCleanedFile(**_data)
        return files
    
    def generate_filepaths(self) -> dict[str: 'filename', Path]:
        return {file: TEST_DIRECTORY.joinpath(file) for file in f.FILES}

    def generate_files_data(self) -> dict[str: 'filename', str: 'data']:
        paths = self.generate_filepaths()

        template = f.TEMPLATE_DATA
        config   = f'''[{DEFAULT_SECTION}]
        {DATE_FORMAT} = %%Y-%%m-%%d
        {EXTENSION} = {f.EXTENSION}

        [{PATH_SECTION}]
        {DESTINATION} = {paths[f.DESTINATION].parent}
        {TEMPLATE} = {paths[f.TEMPLATE]}

        [{FILENAME_SECTION}]
        '''  # double % = escape single %
        return {f.TEMPLATE: template, f.CONFIG: config}


class FilesMixIn:
    '''Create and delete files

    MixIn manage files but do not manage configurations.
    Because of that we need to mock path to config later.
    '''
    required_files = tuple[str: 'filename']()
    config_patched = False

    def create_files(self):
        self.files = dict()
        if self.required_files:
            factory = SelfCleanedFileFactory(self.required_files)
            self.files = factory.produce()
        if f.CONFIG in self.required_files:
            self._patch_config()

    def add_new_file(self, file):
        factory = SelfCleanedFileFactory((file,))
        self.files.update(factory.produce())
        if file == f.CONFIG:
            self._patch_config()

    def _patch_config(self):
        self.config_patched = True
        self.config_path_patcher = patch(
                'configurator.Configurator._get_config_path', 
                return_value=self.files[f.CONFIG].path)
        self.mock_config_path = self.config_path_patcher.start()

    def delete_files(self):
        if self.config_patched:
            self.config_patched = False
            self.config_path_patcher.stop()

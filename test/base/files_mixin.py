from pathlib import Path

import test.base.fixtures as f
from paths import build_path

from constants import (DEFAULT_SECTION, PATH_SECTION, FILENAME_SECTION,
                       DESTINATION, TEMPLATE, DATE_FORMAT, EXTENSION,
                      )


class SelfCleanedFile:
    'Create and delete file on path with given data'

    def __init__(self, path:Path, data:str=''):
        self._path = path
        self._data = data
        self._write_file()

    def _write_file(self):
        with open(self.path, 'w') as f:
            f.write(self.data)

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
        return f'{self.path=}'

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
        return {file: build_path(('test', file)) for file in f.FILES}

    def generate_files_data(self) -> dict[str: 'filename', str: 'data']:
        paths = self.generate_filepaths()

        template = f.TEMPLATE_DATA
        config   = f'''[{DEFAULT_SECTION}]
        {DESTINATION} = {paths[f.DESTINATION].parent}
        {TEMPLATE} = {paths[f.TEMPLATE]}
        {DATE_FORMAT} = %%Y-%%m-%%d
        {EXTENSION} = {f.EXTENSION}

        [{PATH_SECTION}]
        [{FILENAME_SECTION}]
        '''  # double % = escape single %
        return {f.TEMPLATE: template, f.CONFIG: config}


class FilesMixIn:
    files_to_create = tuple[str: 'filename']()

    def create_files(self):
        self.files = dict()
        if self.files_to_create:
            factory = SelfCleanedFileFactory((self.files_to_create))
            self.files = factory.produce()

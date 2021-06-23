from pathlib import Path

from constants import ALL_FILES


class SelfCleanedFile:
    'Create and delete file on path with given data'

    def __init__(self, path:Path, data:str=''):
        self._path = path
        self._data = data
        with open(path, 'w') as f:
            f.write(data)

    @property
    def path(self):
        return self._path

    @property
    def data(self):
        return self._data

    def __repr__(self):
        return f'{self.path=}'

    def __del__(self):
        self._path.unlink()


class SelfCleanedFileFactory:
    def __init__(self, desired_files: tuple[str]):
        self.desired_files = desired_files

    def produce(self) -> dict[str, SelfCleanedFile]:
        datas = self.generate_files_data()
        paths = self.generate_filepaths()

        files = dict()
        for file in self.desired_files:
            _data = {'path': paths[file], 'data': datas.get(file, '')}
            files[file] = SelfCleanedFile(**_data)
        return files
    
    def generate_filepaths(self) -> dict[str: 'filename', Path]:
        base_path = Path().absolute()  # TODO implement build_path()
        path = base_path.joinpath('test')
        return {file: path.joinpath(f'_{file}.md') for file in ALL_FILES}

    def generate_files_data(self) -> dict[str: 'filename', str: 'data']:
        paths = self.generate_filepaths()

        template = '''# Header 1
        ## Header 2
        Test Template text

        - item 1
        - *item 2*
        
        > some quote
        '''
        config   = f'''[DEFAULT]
        destination = {paths['destination'].parent}
        template = {paths['template']}
        date format = %%Y-%%M-%%D

        [PATH]
        [FILENAME]
        '''  # double % = escape single %
        return {'template': template, 'config': config}


class FilesMixIn:
    files_to_create = tuple[str]()

    def setUp(self):
        super().setUp()
        self.files = dict()
        if self.files_to_create:
            factory = SelfCleanedFileFactory((self.files_to_create))
            self.files = factory.produce()

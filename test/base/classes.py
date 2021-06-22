import pathlib
import unittest
from unittest.mock import patch

from test.base.files_mixin import FilesMixIn
from main import Application, PROJECT_DIRECTORY


def build_path(path_parts: tuple[str], start_path=PROJECT_DIRECTORY):
    if type(path_parts) not in (tuple, list):
        raise TypeError(f'Got {path_parts=}, {type(path_parts)=}\n'\
            f'\tpath_parts must be {tuple}[str] or {list}[str]')
    return start_path.joinpath(*path_parts)

def patch_config_path(path_parts:tuple[str]=('test', '_config.md'),
                      start_path=PROJECT_DIRECTORY
                     ):
    path = build_path(path_parts, start_path)
    return patch('main.CONFIG_FILENAME', path)

def patch_sys_argv(path_parts:tuple[str], start_path=PROJECT_DIRECTORY):
    path = build_path(path_parts, start_path)
    return patch('sys.argv', [path])


class BaseTestCase(unittest.TestCase):
    project_directory = pathlib.Path().parent.parent.absolute()

    def setUp(self):
        self.app = Application()


class IntegratedTestCase(FilesMixIn, BaseTestCase):
    pass


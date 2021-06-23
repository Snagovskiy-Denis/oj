from pathlib import Path
from unittest.mock import patch

from constants import BASE_DIRECTORY


def build_path(path_parts:tuple[str],start_path:Path=BASE_DIRECTORY)->Path:
    if type(path_parts) not in (tuple, list):
        raise TypeError(f'Got {path_parts=}, {type(path_parts)=}\n'\
            f'\tpath_parts must be {tuple}[str] or {list}[str]')
    return start_path.joinpath(*path_parts)


def patch_config_path(path_parts:tuple[str]=('test', '_config.md'),
                      start_path=BASE_DIRECTORY
                     ):
    path = build_path(path_parts, start_path)
    return patch('configurator.Configurator._get_config_path', 
            return_value=path)


def patch_sys_argv(path_parts:tuple[str], start_path=BASE_DIRECTORY):
    path = build_path(path_parts, start_path)
    return patch('sys.argv', [path])

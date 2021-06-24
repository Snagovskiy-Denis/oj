from pathlib import Path
from unittest.mock import patch

import test.base.fixtures as f

from paths import build_path, BASE_DIRECTORY, TEST_DIRECTORY


def patch_config_path(
            path_parts:tuple[str]=(f'{f.CONFIG}',),
            start_path=TEST_DIRECTORY
        ):
    path = build_path(path_parts, start_path)
    return patch('configurator.Configurator._get_config_path', 
            return_value=path)


def patch_sys_argv(path_parts:tuple[str], start_path=BASE_DIRECTORY):
    path = build_path(path_parts, start_path)
    return patch('sys.argv', [path])


def patch_is_file(return_value:bool):
    return patch('pathlib.Path.is_file', return_value=return_value)

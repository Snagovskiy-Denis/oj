from pathlib import Path

BASE_DIRECTORY = Path(__file__).parent.absolute()
TEST_DIRECTORY = BASE_DIRECTORY.joinpath('test')


def build_path(path_parts:tuple[str], start_path:Path=BASE_DIRECTORY) -> Path:
    if type(path_parts) not in (tuple, list):
        raise TypeError(f'Got {path_parts=}, {type(path_parts)=}\n'\
            f'\tpath_parts must be {tuple}[str] or {list}[str]')
    return start_path.joinpath(*path_parts)

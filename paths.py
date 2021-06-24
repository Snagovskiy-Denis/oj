from pathlib import Path

BASE_DIRECTORY = Path(__file__).parent.absolute()
TEST_DIRECTORY = BASE_DIRECTORY.joinpath('test')
NON_EXISTING_PATH = TEST_DIRECTORY.joinpath('__non_existing.py__')

'''Non-configurable values'''

from pathlib import Path


# General
APPLICATION_NAME = 'oj'  # stands for open journal
EDITOR = 'EDITOR'

# Paths
BASE_DIRECTORY = Path(__file__).parent.absolute()
TEST_DIRECTORY = BASE_DIRECTORY.joinpath('test')

# Filenames
CONFIG_FILENAME = APPLICATION_NAME + '.ini'

# Mods
DEFAULT_MODE = 'default'
REWRITE_MODE = 'rewrite'

# Config
## Sections
DEFAULT_SECTION = 'DEFAULT'
PATH_SECTION = 'PATH'
FILENAME_SECTION = 'FILENAME'

## Settings
PATH_SETTINGS = DESTINATION, TEMPLATE = ('destination', 'template')

FILENAME_SETTINGS = DATE_FORMAT, EXTENSION = 'date format', 'extension'

ALL_SETTINGS = PATH_SETTINGS, FILENAME_SETTINGS

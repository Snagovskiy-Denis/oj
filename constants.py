'''Non-configurable values'''

from os import getenv
from pathlib import Path


# General
APPLICATION_NAME = 'oj'
EDITOR = 'EDITOR'

# Filenames
CONFIG_FILENAME = f'{APPLICATION_NAME}.ini'
CONFIG_PATH = Path(getenv('HOME')).joinpath('.config', CONFIG_FILENAME)

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

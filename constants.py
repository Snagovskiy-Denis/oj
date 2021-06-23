from pathlib import Path


# General
BASE_DIRECTORY = Path(__file__).parent.absolute()

# Filenames
ALL_FILES = ('template', 'config', 'destination')
CONFIG_FILENAME = 'config.md'  # TODO config.ini

# Mods
DEFAULT = 'DEFAULT'

# Config
PATH_SETTINGS = ('destination', 'template')
FILENAME_SETTINGS = ('date format',)
ALL_SETTINGS = PATH_SETTINGS, FILENAME_SETTINGS

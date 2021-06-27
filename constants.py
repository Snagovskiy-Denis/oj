'''Non-configurable values'''
# General
APPLICATION_NAME = 'oj'
EDITOR = 'EDITOR'  # environment variable

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

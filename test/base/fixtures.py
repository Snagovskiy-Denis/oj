'''Contains default test data'''

from constants import APPLICATION_NAME, TEST_DIRECTORY
from datetime import date


NON_EXISTING_PATH = TEST_DIRECTORY.joinpath('__I_AM_A_LIE__.py')
FAKE_DATE = date(2012, 12, 21)
DATE_FORMAT = '%Y-%m-%d'
EXTENSION = '.md'
EDITOR = 'vi'
FILES = TEMPLATE, DESTINATION, CONFIG = \
            'template.md', 'destination.md', \
            f'{APPLICATION_NAME}.ini'

TEMPLATE_DATA = f'''# Header 1
## Header 2
Test {TEMPLATE.capitalize()} text

- item 1
- *item 2*

> some quote
'''

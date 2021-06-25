'''Contains default test data'''

from constants import APPLICATION_NAME, TEST_DIRECTORY
from datetime import date


NON_EXISTING_PATH = TEST_DIRECTORY.joinpath('__I_AM_A_LIE__.py')
FAKE_DATE = date(2012, 12, 21)
DATE_FORMAT = '%Y-%m-%d'
EXTENSION = '.md'
EDITOR = 'vi'

TEMPLATE = 'template.md'
DESTINATION = FAKE_DATE.isoformat() + EXTENSION
CONFIG = f'{APPLICATION_NAME}.ini'
FILES = TEMPLATE, DESTINATION, CONFIG

TEMPLATE_DATA = f'''# Dear diary
## Todays Evil scheming 
{TEMPLATE}

- [x] write tests for life
- [ ] live a life
- [ ] refactor life
'''

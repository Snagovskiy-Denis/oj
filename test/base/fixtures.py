'''Contains default test data'''

from datetime import date
from pathlib import Path


# Paths
TEST_DIRECTORY = Path(__file__).parent.parent.parent.joinpath('test')
NON_EXISTING_PATH = TEST_DIRECTORY.joinpath('__I_AM_A_LIE__.py')

# Date
FAKE_DATE = date(2012, 12, 21)
DATE_FORMAT = '%Y-%m-%d'

# Misc
EXTENSION = '.md'
EDITOR = 'vi'

# Filenames
TEMPLATE = 'test_template.md'
DESTINATION = f'{FAKE_DATE.isoformat()}{EXTENSION}'
CONFIG = 'test_config.ini'
FILES = TEMPLATE, DESTINATION, CONFIG

# Files data
TEMPLATE_DATA = f'''# Dear diary
## Todays Evil scheming 
{TEMPLATE}

- [x] write tests for life
- [ ] live a life
- [ ] refactor life
'''

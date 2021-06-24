from constants import APPLICATION_NAME
from paths import TEST_DIRECTORY

DATE_FORMAT = '%Y-%m-%d'
EXTENSION = '.md'
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

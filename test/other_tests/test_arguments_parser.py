import sys
from unittest import main
from unittest.mock import patch

from .base import CLIParserTestCase


class ParseSysArgs(CLIParserTestCase):
    def test_parse_multiple_argse(self):
        args = self.cli.parse_args(['--skip'])
        self.assertTrue(args.skip)
        # self.mock_app 
        # self.cli 


if __name__ == '__main__':
    main()

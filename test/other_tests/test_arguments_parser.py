import sys
from unittest import main, skip
from unittest.mock import patch

from .base import CLIParserTestCase

from configurator import DESTINATION, DATE_FORMAT


class ParseSysArgs(CLIParserTestCase):
    def test_parse_multiple_argse(self):
        option1 = f'{DESTINATION}=/tmp'
        option2 = f'{DATE_FORMAT}=%%d %%m'
        args = self.cli.parse_args(['-o', option1, option2, '--skip'])

        self.assertTrue(args.skip)
        expected = {DESTINATION:'/tmp', DATE_FORMAT:'%%d %%m'}
        self.assertEqual(expected, args.option)
        # self.mock_app 
        # self.cli 


class ParseDictActionTestCase(CLIParserTestCase):
    def test_parse_multiple_options(self):
        option1 = 'foo=bar'
        option2 = 'baz=qux'

        args = self.cli.parse_args(['-o', option1, option2])

        self.assertIsInstance(args.option, dict)
        self.assertEqual('bar', args.option['foo'])
        self.assertEqual('qux', args.option['baz'])

    def test_parse_valid_key_value_pair(self):
        option = 'foo=bar'
        args = self.cli.parse_args(['-o', option])
        self.assertEqual('bar', args.option['foo'])

    def test_parse_option_with_spaces_in_key_and_valu(self):
        option = "'foo = bar '"
        args = self.cli.parse_args(['-o', option])
        self.assertEqual('bar', args.option['foo'])

    def test_parse_options_with_space_in_value(self):
        option = "foobar='foo bar'"
        args = self.cli.parse_args(['-o', option])
        self.assertEqual('foo bar', args.option['foobar'])

    def test_parse_options_with_space_in_key(self):
        option = "'foo bar'=foobar"
        args = self.cli.parse_args(['-o', option])
        self.assertEqual('foobar', args.option['foo bar'])

    def test_parse_option_without_pair_raises_error(self):
        with self.assertRaises(Exception):
            self.cli.parse_args(['-o', 'foo'])

    def test_parse_option_without_pair_and_with_end_equal_sign_raises_error(
            self):
        with self.assertRaises(Exception):
            self.cli.parse_args(['-o', 'foo='])

    def test_parse_option_without_pair_and_with_lead_equal_sign_raises_error(
            self):
        with self.assertRaises(Exception):
            self.cli.parse_args(['-o', '=foo'])


if __name__ == '__main__':
    main()

import sys
import unittest
from unittest import skip
from unittest.mock import patch

from constants import DEFAULT
from test.base.classes import BaseTestCase
from test.base.pathcers import patch_sys_argv
        

class ApplicationBehaviorSelectionTest(BaseTestCase):
    @patch_sys_argv(('main.py',))
    def test_get_mode_with_one_sys_argument_set_default_mode(self):
        current_mode = self.app.get_mode()
        self.assertEqual(DEFAULT, current_mode)

    @patch_sys_argv(('main.py',))
    def test_remember_mode_if_number_of_sys_arguments_changed(self):
        initial_mode = self.app.get_mode()

        sys.argv = ['argument'] * 5
        current_mode = self.app.get_mode()
        self.assertEqual(initial_mode, current_mode)

    @skip
    def test_get_mode_with_three_or_more_sys_arguments_raise_exception(self):
        sys.argv = ['script_path', 'mode', 'unknown_argument']
        current_mode = self.app.get_mode()
        self.assertEqual(DEFAULT, current_mode)


if __name__ == '__main__':
    unittest.main()

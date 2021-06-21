import sys
import unittest
from unittest import skip
from unittest.mock import patch

from main import Application


DEFAULT = 'DEFAULT'


class ApplicationBehaviorSelectionTest(unittest.TestCase):
    def setUp(self):
        self.app = Application()

    def tearDown(self):
        pass

    def test_get_mode_with_one_sys_argument_set_default_mode(self):
        sys.argv = ['script_path']
        current_mode = self.app.get_mode()
        self.assertEquals(DEFAULT, current_mode)


if __name__ == '__main__':
    unittest.main()

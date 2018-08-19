import unittest

from scm import _utils as utils
from scm.git import GitClient


class UtilsTestCase(unittest.TestCase):
    def test_raises_exception_if_dvcs_name_is_not_valid(self):
        with self.assertRaises(ValueError):
            utils.get_client_for_dvcs('cheese')

    def test_returns_client_class_when_matches_are_found(self):
        actual_value = utils.get_client_for_dvcs('git')

        self.assertIs(actual_value, GitClient)

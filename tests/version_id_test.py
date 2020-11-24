# Tests if version id uses canonical format
# PEP 440: https://www.python.org/dev/peps/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions

import unittest
import re

from scappamento.__about__ import __version__


def is_canonical(version):
    return re.match(r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9]['
                    r'0-9]*))?(\.dev(0|[1-9][0-9]*))?$', version) is not None


class TestVersionId(unittest.TestCase):
    def test_version_id(self):
        self.assertEqual(True, is_canonical(__version__), 'Version identifier should use canonical format (PEP 440)')


if __name__ == '__main__':
    unittest.main()

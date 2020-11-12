# Tests for Supplier class
# Tests for common usage functions

import unittest

import scappamento.supplier as sc


class TestSupplier(unittest.TestCase):
    def test_constructor(self):  # TODO: config, no_config
        pass

    def test_fix_illegal_sep_quotes(self):
        line = '"asd";"hehehehe;onetwothree";";hihiha";"hahahu;";";hohoho;"'
        sep = ';'
        rep = ','
        line_fixed = '"asd";"hehehehe,onetwothree";",hihiha";"hahahu,";",hohoho,"'
        self.assertEqual(sc.fix_illegal_sep_quotes(line, sep, rep), line_fixed, 'Should convert separators')

    def test_switch_sep(self):
        line = '"asd";"hehehehe,onetwothree";",hihiha";"hahahu,";",hohoho,"'
        sep_old = ';'
        sep_new = ','
        line_switched = '"asd","hehehehe;onetwothree",";hihiha","hahahu;",";hohoho;"'
        self.assertEqual(sc.switch_sep(line, sep_old, sep_new), line_switched, 'Should switch separators')


if __name__ == '__main__':
    unittest.main()

import importlib
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Impl = importlib.import_module(os.environ.get("IMPL", "solution")).ParcelTrackingSystemImpl


class Level1Tests(unittest.TestCase):
    def setUp(self):
        self.s = Impl()

    def test_level_1_case_01_statement_example(self):
        s = self.s
        self.assertIsNone(s.set_tag("parcel1", "status", "in-transit"))
        self.assertEqual(s.get_tag("parcel1", "status"), "in-transit")
        self.assertIsNone(s.set_tag("parcel1", "status", "delivered"))
        self.assertEqual(s.get_tag("parcel1", "status"), "delivered")
        self.assertIs(s.remove_tag("parcel1", "status"), True)
        self.assertIsNone(s.get_tag("parcel1", "status"))
        self.assertIs(s.remove_tag("parcel1", "status"), False)

    def test_level_1_case_02_missing_parcel(self):
        self.assertIsNone(self.s.get_tag("nope", "status"))
        self.assertIs(self.s.remove_tag("nope", "status"), False)

    def test_level_1_case_03_missing_tag_on_existing_parcel(self):
        self.s.set_tag("p1", "status", "x")
        self.assertIsNone(self.s.get_tag("p1", "eta"))
        self.assertIs(self.s.remove_tag("p1", "eta"), False)

    def test_level_1_case_04_parcels_are_independent(self):
        self.s.set_tag("p1", "status", "a")
        self.s.set_tag("p2", "status", "b")
        self.assertEqual(self.s.get_tag("p1", "status"), "a")
        self.assertEqual(self.s.get_tag("p2", "status"), "b")
        self.s.remove_tag("p1", "status")
        self.assertEqual(self.s.get_tag("p2", "status"), "b")

    def test_level_1_case_05_remove_one_tag_keeps_others(self):
        self.s.set_tag("p1", "status", "x")
        self.s.set_tag("p1", "eta", "mon")
        self.assertIs(self.s.remove_tag("p1", "status"), True)
        self.assertEqual(self.s.get_tag("p1", "eta"), "mon")

    def test_level_1_case_06_empty_string_value_is_a_value(self):
        # `if value:` style truthiness checks turn "" into None — a classic hidden-test catch.
        self.s.set_tag("p1", "note", "")
        self.assertEqual(self.s.get_tag("p1", "note"), "")
        self.assertIs(self.s.remove_tag("p1", "note"), True)

    def test_level_1_case_07_set_after_remove(self):
        self.s.set_tag("p1", "status", "x")
        self.s.remove_tag("p1", "status")
        self.s.set_tag("p1", "status", "y")
        self.assertEqual(self.s.get_tag("p1", "status"), "y")

    def test_level_1_case_08_returns_bool_not_truthy(self):
        self.s.set_tag("p1", "status", "x")
        self.assertIsInstance(self.s.remove_tag("p1", "status"), bool)
        self.assertIsInstance(self.s.remove_tag("p1", "status"), bool)


if __name__ == "__main__":
    unittest.main()

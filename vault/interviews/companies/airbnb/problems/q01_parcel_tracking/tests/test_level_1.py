"""Level 1 — 10 tests, like the real level_1_tests.py. Cases 01-04 are copied from the assessment photos
(case 04's last two cut-off assertions omitted); cases 05-10 are ours."""
import importlib
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Impl = importlib.import_module(os.environ.get("IMPL", "solution")).ParcelTrackingSystemImpl


class Level1Tests(unittest.TestCase):
    def setUp(self):
        self.tracker = Impl()

    # ---- verbatim from the photos ---------------------------------------------------------

    def test_level_1_case_01_simple_set_and_get_1(self):
        self.tracker.set_tag('parcel1', 'destination_city', 'Annapolis')
        self.tracker.set_tag('parcel2', 'tracking_number', '0123')
        self.assertEqual(self.tracker.get_tag('parcel1', 'destination_city'), 'Annapolis')

    def test_level_1_case_02_simple_set_and_get_2(self):
        self.assertIsNone(self.tracker.get_tag('parcel4', 'service'))
        self.tracker.set_tag('parcel4', 'service', 'express')
        self.assertEqual(self.tracker.get_tag('parcel4', 'service'), 'express')
        self.assertEqual(self.tracker.get_tag('parcel4', 'service'), 'express')

    def test_level_1_case_03_simple_set_get_and_delete(self):
        self.tracker.set_tag('parcel5', 'status', 'in-transit')
        self.assertEqual(self.tracker.get_tag('parcel5', 'status'), 'in-transit')
        self.assertTrue(self.tracker.remove_tag('parcel5', 'status'))
        self.assertIsNone(self.tracker.get_tag('parcel5', 'status'))

    def test_level_1_case_04_multiple_parcels_with_same_tag(self):
        self.tracker.set_tag('parcel6', 'recipient_name', 'HubA')
        self.tracker.set_tag('parcel6', 'sender_name', 'HubB')
        self.tracker.set_tag('sender_name', 'parcel6', 'error')  # swapped on purpose: a different parcel
        self.assertEqual(self.tracker.get_tag('parcel6', 'sender_name'), 'HubB')
        self.assertEqual(self.tracker.get_tag('parcel6', 'recipient_name'), 'HubA')
        self.assertIsNone(self.tracker.get_tag('parcel6', 'parcel6'))

    # ---- ours -------------------------------------------------------------------------------

    def test_level_1_case_05_statement_example(self):
        t = self.tracker
        self.assertIsNone(t.set_tag("parcel1", "status", "in-transit"))
        self.assertEqual(t.get_tag("parcel1", "status"), "in-transit")
        self.assertIsNone(t.set_tag("parcel1", "status", "delivered"))
        self.assertEqual(t.get_tag("parcel1", "status"), "delivered")
        self.assertIs(t.remove_tag("parcel1", "status"), True)
        self.assertIsNone(t.get_tag("parcel1", "status"))
        self.assertIs(t.remove_tag("parcel1", "status"), False)

    def test_level_1_case_06_remove_on_missing_parcel_or_tag(self):
        self.assertIs(self.tracker.remove_tag("nope", "status"), False)
        self.tracker.set_tag("p1", "status", "x")
        self.assertIs(self.tracker.remove_tag("p1", "eta"), False)
        self.assertIsNone(self.tracker.get_tag("p1", "eta"))

    def test_level_1_case_07_parcels_are_independent(self):
        self.tracker.set_tag("p1", "status", "a")
        self.tracker.set_tag("p2", "status", "b")
        self.tracker.remove_tag("p1", "status")
        self.assertIsNone(self.tracker.get_tag("p1", "status"))
        self.assertEqual(self.tracker.get_tag("p2", "status"), "b")

    def test_level_1_case_08_remove_one_tag_keeps_others(self):
        self.tracker.set_tag("p1", "status", "x")
        self.tracker.set_tag("p1", "eta", "mon")
        self.assertIs(self.tracker.remove_tag("p1", "status"), True)
        self.assertEqual(self.tracker.get_tag("p1", "eta"), "mon")

    def test_level_1_case_09_empty_string_value_is_a_value(self):
        # `if value:` style truthiness checks turn "" into None.
        self.tracker.set_tag("p1", "note", "")
        self.assertEqual(self.tracker.get_tag("p1", "note"), "")
        self.assertIs(self.tracker.remove_tag("p1", "note"), True)

    def test_level_1_case_10_set_after_remove(self):
        self.tracker.set_tag("p1", "status", "x")
        self.tracker.remove_tag("p1", "status")
        self.tracker.set_tag("p1", "status", "y")
        self.assertEqual(self.tracker.get_tag("p1", "status"), "y")


if __name__ == "__main__":
    unittest.main()

"""Level 2 — (reconstructed) method names and output format; see problem.md."""
import importlib
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Impl = importlib.import_module(os.environ.get("IMPL", "solution")).ParcelTrackingSystemImpl


class Level2Tests(unittest.TestCase):
    def setUp(self):
        self.s = Impl()
        for tag, value in [("status", "in-transit"), ("eta", "mon"), ("carrier", "ups"), ("city_to", "SF"),
                           ("city_from", "NYC")]:
            self.s.set_tag("p1", tag, value)

    def test_level_2_case_01_example(self):
        self.assertEqual(
            self.s.list_tags("p1"),
            ["carrier(ups)", "city_from(NYC)", "city_to(SF)", "eta(mon)", "status(in-transit)"],
        )
        self.assertEqual(self.s.list_tags_by_prefix("p1", "city"), ["city_from(NYC)", "city_to(SF)"])

    def test_level_2_case_02_missing_parcel_is_empty_list(self):
        self.assertEqual(self.s.list_tags("nope"), [])
        self.assertEqual(self.s.list_tags_by_prefix("nope", "c"), [])

    def test_level_2_case_03_parcel_emptied_by_removes(self):
        self.s.set_tag("p2", "a", "1")
        self.s.remove_tag("p2", "a")
        self.assertEqual(self.s.list_tags("p2"), [])

    def test_level_2_case_04_sorted_by_tag_not_insertion_order(self):
        s = Impl()
        for tag in ["b", "ab", "a", "B"]:
            s.set_tag("p", tag, tag.upper())
        # Plain lexicographic (code point) order: uppercase sorts before lowercase.
        self.assertEqual(s.list_tags("p"), ["B(B)", "a(A)", "ab(AB)", "b(B)"])

    def test_level_2_case_05_prefix_no_match(self):
        self.assertEqual(self.s.list_tags_by_prefix("p1", "zzz"), [])

    def test_level_2_case_06_empty_prefix_is_everything(self):
        self.assertEqual(self.s.list_tags_by_prefix("p1", ""), self.s.list_tags("p1"))

    def test_level_2_case_07_prefix_is_prefix_not_substring(self):
        # "to" appears inside "city_to" but is not its prefix.
        self.assertEqual(self.s.list_tags_by_prefix("p1", "to"), [])
        self.assertEqual(self.s.list_tags_by_prefix("p1", "city_to"), ["city_to(SF)"])

    def test_level_2_case_08_reflects_overwrite_and_remove(self):
        self.s.set_tag("p1", "eta", "tue")
        self.s.remove_tag("p1", "carrier")
        self.assertEqual(
            self.s.list_tags("p1"),
            ["city_from(NYC)", "city_to(SF)", "eta(tue)", "status(in-transit)"],
        )


if __name__ == "__main__":
    unittest.main()

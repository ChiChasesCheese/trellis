"""Level 3 — spec verbatim from the photos. Cases 01-02 are the statement's examples; the rest are ours."""
import importlib
import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Impl = importlib.import_module(os.environ.get("IMPL", "solution")).ParcelTrackingSystemImpl


class Level3Tests(unittest.TestCase):
    def setUp(self):
        self.s = Impl()

    def test_level_3_case_01_statement_example_hold(self):
        s = self.s
        s.set_tag_with_hold("parcel1", "status", "held", 100, 50)  # expires at 150
        self.assertEqual(s.get_tag_at("parcel1", "status", 120), "held")
        self.assertIsNone(s.get_tag_at("parcel1", "status", 150))
        self.assertIsNone(s.get_tag_at("parcel1", "status", 180))

    def test_level_3_case_02_statement_example_remove(self):
        s = self.s
        s.set_tag_with_hold("parcel1", "status", "held", 20, 60)  # expires at 80
        self.assertIs(s.remove_tag_at("parcel1", "status", 50), True)
        # The statement goes back to ts=20 here, despite promising non-decreasing timestamps.
        s.set_tag_with_hold("parcel1", "hold_reason", "customs", 20, 60)  # expires at 80
        self.assertIs(s.remove_tag_at("parcel1", "hold_reason", 80), False)
        self.assertIs(s.remove_tag_at("parcel1", "priority", 80), False)  # timestamp cut off in the photo

    def test_level_3_case_03_ttl_zero_never_expires(self):
        self.s.set_tag_with_hold("p1", "a", "x", 5, 0)
        self.assertEqual(self.s.get_tag_at("p1", "a", 5), "x")
        self.assertEqual(self.s.get_tag_at("p1", "a", 10**9), "x")
        self.assertEqual(self.s.list_tags_at("p1", 10**9), ["a(x)"])

    def test_level_3_case_04_expiry_boundary_is_exclusive(self):
        self.s.set_tag_with_hold("p1", "a", "x", 5, 3)  # [5, 8)
        self.assertEqual(self.s.get_tag_at("p1", "a", 7), "x")
        self.assertIsNone(self.s.get_tag_at("p1", "a", 8))

    def test_level_3_case_05_set_without_ttl_clears_old_ttl(self):
        self.s.set_tag_with_hold("p1", "a", "x", 1, 5)  # would expire at 6
        self.s.set_tag_at("p1", "a", "y", 2)  # "does not expire unless overwritten"
        self.assertEqual(self.s.get_tag_at("p1", "a", 1000), "y")

    def test_level_3_case_06_overwrite_resets_ttl(self):
        self.s.set_tag_with_hold("p1", "a", "x", 1, 5)  # [1, 6)
        self.s.set_tag_with_hold("p1", "a", "y", 4, 10)  # [4, 14)
        self.assertEqual(self.s.get_tag_at("p1", "a", 13), "y")
        self.assertIsNone(self.s.get_tag_at("p1", "a", 14))

    def test_level_3_case_07_remove_expired_is_false_and_set_again_works(self):
        self.s.set_tag_with_hold("p1", "a", "x", 1, 2)  # [1, 3)
        self.assertIs(self.s.remove_tag_at("p1", "a", 3), False)
        self.s.set_tag_at("p1", "a", "z", 4)
        self.assertEqual(self.s.get_tag_at("p1", "a", 5), "z")

    def test_level_3_case_08_list_at_filters_expired(self):
        s = self.s
        s.set_tag_with_hold("p1", "city_to", "SF", 1, 5)  # [1, 6)
        s.set_tag_at("p1", "city_from", "NYC", 2)
        s.set_tag_with_hold("p1", "carrier", "ups", 3, 100)
        self.assertEqual(s.list_tags_at("p1", 5), ["carrier(ups)", "city_from(NYC)", "city_to(SF)"])
        self.assertEqual(s.list_tags_by_prefix_at("p1", "city", 6), ["city_from(NYC)"])
        self.assertEqual(s.list_tags_at("p1", 103), ["city_from(NYC)"])

    def test_level_3_case_09_equal_timestamps_are_allowed(self):
        # Timestamps are non-decreasing, not strictly increasing.
        s = self.s
        s.set_tag_at("p1", "a", "x", 7)
        s.set_tag_at("p1", "a", "y", 7)
        self.assertEqual(s.get_tag_at("p1", "a", 7), "y")
        self.assertIs(s.remove_tag_at("p1", "a", 7), True)

    def test_level_3_case_10_perf_within_time_limit(self):
        # The real tests carry @timeout(0.4): 0.4 s per test. A plain dict-of-dicts design needs ~0.03 s here.
        s = self.s
        start = time.perf_counter()
        ts = 0
        for i in range(50_000):
            ts += 1
            s.set_tag_with_hold(f"p{i % 1000}", f"t{i % 50}", str(i), ts, 500)
        for i in range(5_000):
            ts += 1
            s.get_tag_at(f"p{i % 1000}", f"t{i % 50}", ts)
            if i % 10 == 0:
                s.list_tags_by_prefix_at(f"p{i % 1000}", "t1", ts)
        self.assertLess(time.perf_counter() - start, 0.4)


if __name__ == "__main__":
    unittest.main()

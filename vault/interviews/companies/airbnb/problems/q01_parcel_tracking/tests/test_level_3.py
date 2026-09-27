"""Level 3 — (reconstructed) method names; TTL semantics [timestamp, timestamp + ttl) from the isomorph."""
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

    def test_level_3_case_01_example(self):
        s = self.s
        s.set_tag_at_with_ttl("p1", "status", "in-transit", 1, 10)  # alive on [1, 11)
        self.assertEqual(s.get_tag_at("p1", "status", 10), "in-transit")
        self.assertIsNone(s.get_tag_at("p1", "status", 11))
        s.set_tag_at("p1", "eta", "mon", 12)
        self.assertEqual(s.list_tags_at("p1", 12), ["eta(mon)"])
        self.assertIs(s.remove_tag_at("p1", "status", 13), False)
        self.assertIs(s.remove_tag_at("p1", "eta", 14), True)

    def test_level_3_case_02_expiry_boundary_is_exclusive(self):
        self.s.set_tag_at_with_ttl("p1", "a", "x", 5, 3)  # [5, 8)
        self.assertEqual(self.s.get_tag_at("p1", "a", 7), "x")
        self.assertIsNone(self.s.get_tag_at("p1", "a", 8))

    def test_level_3_case_03_set_without_ttl_clears_old_ttl(self):
        self.s.set_tag_at_with_ttl("p1", "a", "x", 1, 5)  # would expire at 6
        self.s.set_tag_at("p1", "a", "y", 2)  # now permanent
        self.assertEqual(self.s.get_tag_at("p1", "a", 1000), "y")

    def test_level_3_case_04_overwrite_resets_ttl(self):
        self.s.set_tag_at_with_ttl("p1", "a", "x", 1, 5)  # [1, 6)
        self.s.set_tag_at_with_ttl("p1", "a", "y", 4, 10)  # [4, 14)
        self.assertEqual(self.s.get_tag_at("p1", "a", 13), "y")
        self.assertIsNone(self.s.get_tag_at("p1", "a", 14))

    def test_level_3_case_05_remove_expired_is_false_and_set_again_works(self):
        self.s.set_tag_at_with_ttl("p1", "a", "x", 1, 2)  # [1, 3)
        self.assertIs(self.s.remove_tag_at("p1", "a", 3), False)
        self.s.set_tag_at("p1", "a", "z", 4)
        self.assertEqual(self.s.get_tag_at("p1", "a", 5), "z")

    def test_level_3_case_06_list_at_filters_expired(self):
        s = self.s
        s.set_tag_at_with_ttl("p1", "city_to", "SF", 1, 5)  # [1, 6)
        s.set_tag_at("p1", "city_from", "NYC", 2)
        s.set_tag_at_with_ttl("p1", "carrier", "ups", 3, 100)
        self.assertEqual(s.list_tags_at("p1", 5), ["carrier(ups)", "city_from(NYC)", "city_to(SF)"])
        self.assertEqual(s.list_tags_by_prefix_at("p1", "city", 6), ["city_from(NYC)"])
        self.assertEqual(s.list_tags_at("p1", 103), ["city_from(NYC)"])

    def test_level_3_case_07_all_tags_expired_means_empty(self):
        self.s.set_tag_at_with_ttl("p1", "a", "x", 1, 1)
        self.assertEqual(self.s.list_tags_at("p1", 2), [])
        self.assertIsNone(self.s.get_tag_at("p1", "a", 2))

    def test_level_3_case_08_perf_within_time_limit(self):
        # CodeSignal's execution limit is 3 s per test; a sane O(tags) design should need well under 1 s.
        s = self.s
        start = time.perf_counter()
        ts = 0
        for i in range(50_000):
            ts += 1
            s.set_tag_at_with_ttl(f"p{i % 1000}", f"t{i % 50}", str(i), ts, 500)
        for i in range(5_000):
            ts += 1
            s.get_tag_at(f"p{i % 1000}", f"t{i % 50}", ts)
            if i % 10 == 0:
                s.list_tags_by_prefix_at(f"p{i % 1000}", "t1", ts)
        self.assertLess(time.perf_counter() - start, 3.0)


if __name__ == "__main__":
    unittest.main()

"""Level 4 — spec verbatim from the photos. Cases 01-02 come from the statement's examples; the rest are ours."""
import importlib
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Impl = importlib.import_module(os.environ.get("IMPL", "solution")).ParcelTrackingSystemImpl


class Level4Tests(unittest.TestCase):
    def setUp(self):
        self.s = Impl()

    def test_level_4_case_01_statement_example_1_visible_part(self):
        s = self.s
        s.set_tag_with_hold("parcel1", "status", "held", 100, 100)  # expires at 200
        self.assertEqual(s.checkpoint(120), 1)

    def test_level_4_case_02_statement_example_shift_uses_checkpoint_timestamp(self):
        s = self.s
        s.set_tag_with_hold("parcel1", "route_east", "active", 30, 70)  # expires at 100
        self.assertEqual(s.checkpoint(31), 1)
        s.set_tag_with_hold("parcel1", "route_west", "queued", 35, 25)  # expires at 60
        self.assertEqual(s.checkpoint(41), 1)
        self.assertIsNone(s.restore_checkpoint(110, 35))  # checkpoint at 31, delta = 79
        self.assertIsNone(s.get_tag_at("parcel1", "route_west", 115))
        self.assertEqual(s.get_tag_at("parcel1", "route_east", 115), "active")  # expires at 179
        self.assertEqual(s.get_tag_at("parcel1", "route_east", 178), "active")
        self.assertIsNone(s.get_tag_at("parcel1", "route_east", 179))

    def test_level_4_case_03_no_checkpoint_before_means_no_effect(self):
        s = self.s
        s.set_tag_at("p1", "a", "x", 5)
        s.checkpoint(10)
        s.set_tag_at("p1", "b", "y", 11)
        self.assertIsNone(s.restore_checkpoint(12, 9))  # only checkpoint is at 10 > 9
        self.assertEqual(s.list_tags_at("p1", 12), ["a(x)", "b(y)"])

    def test_level_4_case_04_count_ignores_expired_and_empty_parcels(self):
        s = self.s
        s.set_tag_with_hold("p1", "a", "x", 1, 5)  # [1, 6)
        s.set_tag_at("p2", "b", "y", 2)
        s.set_tag_at("p3", "c", "z", 3)
        s.remove_tag_at("p3", "c", 4)
        self.assertEqual(s.checkpoint(6), 1)
        self.assertEqual(Impl().checkpoint(1), 0)

    def test_level_4_case_05_restore_picks_latest_at_or_before(self):
        s = self.s
        s.set_tag_at("p1", "v", "one", 1)
        s.checkpoint(3)
        s.set_tag_at("p1", "v", "two", 5)
        s.checkpoint(7)
        s.set_tag_at("p1", "v", "three", 9)
        s.restore_checkpoint(10, 6)  # latest checkpoint <= 6 is the one at 3
        self.assertEqual(s.get_tag_at("p1", "v", 11), "one")
        s.restore_checkpoint(12, 7)  # exactly at a checkpoint time counts
        self.assertEqual(s.get_tag_at("p1", "v", 13), "two")

    def test_level_4_case_06_checkpoint_is_isolated_from_later_writes(self):
        # A shallow copy of the outer dict shares the inner tag dicts: later writes leak into the checkpoint.
        s = self.s
        s.set_tag_at("p1", "a", "x", 1)
        s.checkpoint(2)
        s.set_tag_at("p1", "a", "changed", 3)
        s.set_tag_at("p1", "b", "new", 4)
        s.restore_checkpoint(5, 2)
        self.assertEqual(s.list_tags_at("p1", 6), ["a(x)"])

    def test_level_4_case_07_restoring_twice_gives_same_state(self):
        # Restoring by pointing live state at the saved object lets later writes corrupt the checkpoint.
        s = self.s
        s.set_tag_at("p1", "a", "x", 1)
        s.checkpoint(2)
        s.restore_checkpoint(3, 2)
        s.set_tag_at("p1", "a", "dirty", 4)
        s.set_tag_at("p1", "b", "extra", 5)
        s.restore_checkpoint(6, 2)
        self.assertEqual(s.list_tags_at("p1", 7), ["a(x)"])

    def test_level_4_case_08_no_ttl_and_ttl_zero_stay_permanent(self):
        s = self.s
        s.set_tag_at("p1", "a", "x", 1)
        s.set_tag_with_hold("p1", "b", "y", 2, 0)
        s.checkpoint(3)
        s.restore_checkpoint(50, 3)
        self.assertEqual(s.list_tags_at("p1", 10**9), ["a(x)", "b(y)"])

    def test_level_4_case_09_expired_at_checkpoint_stays_expired(self):
        s = self.s
        s.set_tag_with_hold("p1", "a", "x", 1, 2)  # [1, 3)
        s.set_tag_at("p1", "b", "y", 2)
        s.checkpoint(3)  # a is already dead at 3
        s.restore_checkpoint(4, 3)
        self.assertEqual(s.list_tags_at("p1", 4), ["b(y)"])

    def test_level_4_case_10_restore_drops_parcels_created_after_checkpoint(self):
        s = self.s
        s.set_tag_at("p1", "a", "x", 1)
        s.checkpoint(2)
        s.set_tag_at("p9", "z", "late", 3)
        s.restore_checkpoint(4, 2)
        self.assertEqual(s.list_tags_at("p9", 5), [])
        self.assertEqual(s.checkpoint(6), 1)


if __name__ == "__main__":
    unittest.main()

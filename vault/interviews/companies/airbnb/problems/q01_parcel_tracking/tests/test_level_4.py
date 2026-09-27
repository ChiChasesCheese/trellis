"""Level 4 — (reconstructed) names and TTL-recalculation rule; see problem.md."""
import importlib
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Impl = importlib.import_module(os.environ.get("IMPL", "solution")).ParcelTrackingSystemImpl


class Level4Tests(unittest.TestCase):
    def setUp(self):
        self.s = Impl()

    def test_level_4_case_01_example(self):
        s = self.s
        s.set_tag_at_with_ttl("p1", "a", "x", 1, 10)  # [1, 11)
        s.set_tag_at("p2", "b", "y", 2)
        self.assertEqual(s.checkpoint(3), 2)  # p1.a has 11 - 3 = 8 left
        s.set_tag_at("p1", "c", "z", 4)
        self.assertIs(s.remove_tag_at("p2", "b", 5), True)
        self.assertIsNone(s.restore(20, 3))  # p1.a re-anchored: expires at 20 + 8 = 28
        self.assertEqual(s.get_tag_at("p1", "a", 27), "x")
        self.assertIsNone(s.get_tag_at("p1", "a", 28))
        self.assertIsNone(s.get_tag_at("p1", "c", 29))
        self.assertEqual(s.get_tag_at("p2", "b", 30), "y")

    def test_level_4_case_02_count_ignores_expired_and_empty_parcels(self):
        s = self.s
        s.set_tag_at_with_ttl("p1", "a", "x", 1, 5)  # [1, 6)
        s.set_tag_at("p2", "b", "y", 2)
        s.set_tag_at("p3", "c", "z", 3)
        s.remove_tag_at("p3", "c", 4)
        self.assertEqual(s.checkpoint(6), 1)

    def test_level_4_case_03_checkpoint_on_empty_system(self):
        self.assertEqual(self.s.checkpoint(1), 0)

    def test_level_4_case_04_restore_picks_latest_at_or_before(self):
        s = self.s
        s.set_tag_at("p1", "v", "one", 1)
        s.checkpoint(3)
        s.set_tag_at("p1", "v", "two", 5)
        s.checkpoint(7)
        s.set_tag_at("p1", "v", "three", 9)
        s.restore(10, 6)  # latest checkpoint <= 6 is the one at 3
        self.assertEqual(s.get_tag_at("p1", "v", 11), "one")
        s.restore(12, 7)  # exactly at a checkpoint time counts
        self.assertEqual(s.get_tag_at("p1", "v", 13), "two")
        s.restore(14, 100)
        self.assertEqual(s.get_tag_at("p1", "v", 15), "two")

    def test_level_4_case_05_checkpoint_is_isolated_from_later_writes(self):
        # A shallow copy of the outer dict shares the inner tag dicts: later writes leak into the checkpoint.
        s = self.s
        s.set_tag_at("p1", "a", "x", 1)
        s.checkpoint(2)
        s.set_tag_at("p1", "a", "changed", 3)
        s.set_tag_at("p1", "b", "new", 4)
        s.restore(5, 2)
        self.assertEqual(s.list_tags_at("p1", 6), ["a(x)"])

    def test_level_4_case_06_restoring_twice_gives_same_state(self):
        # Restoring by pointing live state at the snapshot object lets later writes corrupt the snapshot.
        s = self.s
        s.set_tag_at("p1", "a", "x", 1)
        s.checkpoint(2)
        s.restore(3, 2)
        s.set_tag_at("p1", "a", "dirty", 4)
        s.remove_tag_at("p1", "a", 5)
        s.restore(6, 2)
        self.assertEqual(s.get_tag_at("p1", "a", 7), "x")

    def test_level_4_case_07_expired_at_checkpoint_does_not_come_back(self):
        s = self.s
        s.set_tag_at_with_ttl("p1", "a", "x", 1, 2)  # [1, 3)
        s.set_tag_at("p1", "b", "y", 2)
        s.checkpoint(3)  # a is already dead at 3
        s.restore(4, 3)
        self.assertEqual(s.list_tags_at("p1", 4), ["b(y)"])

    def test_level_4_case_08_restore_drops_parcels_created_after_checkpoint(self):
        s = self.s
        s.set_tag_at("p1", "a", "x", 1)
        s.checkpoint(2)
        s.set_tag_at("p9", "z", "late", 3)
        s.restore(4, 2)
        self.assertEqual(s.list_tags_at("p9", 5), [])
        self.assertEqual(s.checkpoint(6), 1)


if __name__ == "__main__":
    unittest.main()

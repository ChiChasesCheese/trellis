"""Level 3 — transfer / accept_transfer (reconstructed). Case 01 is the GitHub statement example; the rest are ours.
The 24 h boundary (case 05) is the half-open reading [t, t + 86400000); one GitHub solution accepts at exactly t + 1 day."""
import importlib
import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Impl = importlib.import_module(os.environ.get("IMPL", "solution")).BankingSystemImpl

DAY = 86400000


class Level3Tests(unittest.TestCase):
    def setUp(self):
        self.system = Impl()
        self.system.create_account(1, "a")
        self.system.create_account(2, "b")
        self.system.deposit(3, "a", 1000)

    def test_level_3_case_01_statement_example(self):
        s = Impl()
        s.create_account(1, "account1")
        s.create_account(2, "account2")
        s.deposit(3, "account1", 2000)
        self.assertEqual(s.transfer(4, "account1", "account2", 1000), "transfer1")
        self.assertIs(s.accept_transfer(5, "account2", "transfer1"), True)
        self.assertEqual(s.deposit(6, "account2", 0), 1000)
        self.assertEqual(s.deposit(7, "account1", 0), 1000)

    def test_level_3_case_02_money_is_held_until_accepted(self):
        s = self.system
        self.assertEqual(s.transfer(4, "a", "b", 400), "transfer1")
        self.assertEqual(s.deposit(5, "a", 0), 600)    # left the source at once
        self.assertEqual(s.deposit(6, "b", 0), 0)      # not in the target yet
        self.assertIsNone(s.pay(7, "a", 601))          # held money cannot be spent
        s.accept_transfer(8, "b", "transfer1")
        self.assertEqual(s.deposit(9, "b", 0), 400)

    def test_level_3_case_03_invalid_transfers_return_none(self):
        s = self.system
        self.assertIsNone(s.transfer(4, "a", "a", 10))
        self.assertIsNone(s.transfer(5, "a", "ghost", 10))
        self.assertIsNone(s.transfer(6, "ghost", "a", 10))
        self.assertIsNone(s.transfer(7, "a", "b", 1001))
        # failed attempts do not consume an ordinal
        self.assertEqual(s.transfer(8, "a", "b", 1000), "transfer1")
        self.assertEqual(s.transfer(9, "b", "a", 0), "transfer2")

    def test_level_3_case_04_accept_rules(self):
        s = self.system
        s.transfer(4, "a", "b", 100)
        self.assertIs(s.accept_transfer(5, "a", "transfer1"), False)       # not the target
        self.assertIs(s.accept_transfer(6, "b", "transfer9"), False)       # no such transfer
        self.assertIs(s.accept_transfer(7, "b", "transfer1"), True)
        self.assertIs(s.accept_transfer(8, "b", "transfer1"), False)       # already accepted
        self.assertEqual(s.deposit(9, "b", 0), 100)

    def test_level_3_case_05_expiry_boundary_is_exclusive(self):
        s = self.system
        s.transfer(10, "a", "b", 100)
        s.transfer(11, "a", "b", 100)
        self.assertIs(s.accept_transfer(10 + DAY - 1, "b", "transfer1"), True)    # last valid millisecond
        self.assertIs(s.accept_transfer(11 + DAY, "b", "transfer2"), False)       # expired at exactly t + 1 day

    def test_level_3_case_06_expired_money_returns_to_source(self):
        s = self.system
        s.transfer(4, "a", "b", 300)
        self.assertEqual(s.deposit(5, "a", 0), 700)
        self.assertEqual(s.deposit(4 + DAY, "a", 0), 1000)    # refunded before the deposit is applied
        self.assertEqual(s.deposit(4 + DAY + 1, "b", 0), 0)

    def test_level_3_case_07_refund_visible_to_pay_and_transfer(self):
        s = self.system
        s.transfer(4, "a", "b", 1000)
        self.assertIsNone(s.pay(5, "a", 1))
        self.assertEqual(s.pay(4 + DAY, "a", 1000), 0)        # pay sees the refund first
        s.deposit(4 + DAY + 1, "a", 50)
        s.transfer(4 + DAY + 2, "a", "b", 50)
        self.assertEqual(s.transfer(4 + 2 * DAY + 2, "a", "b", 50), "transfer3")  # refund visible to transfer

    def test_level_3_case_08_activity_counts_on_accept_only(self):
        s = self.system
        s.create_account(4, "c")
        s.transfer(5, "a", "b", 200)
        s.transfer(6, "a", "c", 300)
        self.assertEqual(s.top_activity(7, 3), ["a(1000)", "b(0)", "c(0)"])   # pending: nothing yet
        s.accept_transfer(8, "b", "transfer1")
        self.assertEqual(s.top_activity(9, 3), ["a(1200)", "b(200)", "c(0)"])
        self.assertEqual(s.top_activity(6 + DAY, 3), ["a(1200)", "b(200)", "c(0)"])  # expired: never counts

    def test_level_3_case_09_target_can_spend_after_accept(self):
        s = self.system
        s.transfer(4, "a", "b", 1000)
        s.accept_transfer(5, "b", "transfer1")
        self.assertEqual(s.transfer(6, "b", "a", 1000), "transfer2")
        self.assertIs(s.accept_transfer(7, "a", "transfer2"), True)
        self.assertEqual(s.deposit(8, "a", 0), 1000)

    def test_level_3_case_10_perf_within_time_limit(self):
        s = Impl()
        start = time.perf_counter()
        ts = 0
        for i in range(200):
            ts += 1
            s.create_account(ts, f"acc{i}")
            ts += 1
            s.deposit(ts, f"acc{i}", 10 ** 6)
        for i in range(2000):
            ts += 1
            tid = s.transfer(ts, f"acc{i % 200}", f"acc{(i + 1) % 200}", 1)
            if i % 2:
                ts += 1
                s.accept_transfer(ts, f"acc{(i + 1) % 200}", tid)
        self.assertLess(time.perf_counter() - start, 0.4)


if __name__ == "__main__":
    unittest.main()

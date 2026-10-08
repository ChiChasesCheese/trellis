"""Level 4 — merge_accounts / get_balance (reconstructed). Case 01 is the GitHub statement example; the rest are ours."""
import importlib
import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Impl = importlib.import_module(os.environ.get("IMPL", "solution")).BankingSystemImpl

DAY = 86400000


class Level4Tests(unittest.TestCase):
    def setUp(self):
        self.system = Impl()

    def _two_accounts(self):
        s = self.system
        s.create_account(1, "a")
        s.create_account(2, "b")
        s.deposit(3, "a", 1000)
        s.deposit(4, "b", 500)
        return s

    def test_level_4_case_01_statement_example(self):
        s = self.system
        s.create_account(1, "account1")
        s.create_account(2, "account2")
        s.deposit(3, "account1", 1000)
        s.deposit(4, "account2", 1000)
        self.assertIs(s.merge_accounts(5, "account1", "account2"), True)
        self.assertEqual(s.get_balance(6, "account1", 3), 1000)
        self.assertIsNone(s.get_balance(7, "account2", 6))
        self.assertEqual(s.get_balance(8, "account1", 5), 2000)

    def test_level_4_case_02_invalid_merges(self):
        s = self._two_accounts()
        self.assertIs(s.merge_accounts(5, "a", "a"), False)
        self.assertIs(s.merge_accounts(6, "a", "ghost"), False)
        self.assertIs(s.merge_accounts(7, "ghost", "a"), False)
        self.assertEqual(s.deposit(8, "a", 0), 1000)
        self.assertEqual(s.deposit(9, "b", 0), 500)

    def test_level_4_case_03_merged_id_is_gone_and_activity_moves(self):
        s = self._two_accounts()
        s.merge_accounts(5, "a", "b")
        self.assertIsNone(s.deposit(6, "b", 10))
        self.assertIsNone(s.pay(7, "b", 0))
        self.assertEqual(s.top_activity(8, 5), ["a(1500)"])
        self.assertEqual(s.deposit(9, "a", 0), 1500)
        self.assertIs(s.create_account(10, "b"), True)      # the id is free again
        self.assertEqual(s.top_activity(11, 5), ["a(1500)", "b(0)"])

    def test_level_4_case_04_outgoing_transfers_of_merged_account_cancelled(self):
        s = self._two_accounts()
        s.create_account(5, "c")
        tid = s.transfer(6, "b", "c", 300)
        s.merge_accounts(7, "a", "b")
        self.assertIs(s.accept_transfer(8, "c", tid), False)
        self.assertEqual(s.deposit(9, "a", 0), 1500)         # the held 300 came back with b
        self.assertEqual(s.deposit(10, "c", 0), 0)

    def test_level_4_case_05_incoming_transfers_redirected(self):
        s = self._two_accounts()
        s.create_account(5, "c")
        s.deposit(6, "c", 200)
        tid = s.transfer(7, "c", "b", 200)
        s.merge_accounts(8, "a", "b")
        self.assertIs(s.accept_transfer(9, "b", tid), False)
        self.assertIs(s.accept_transfer(10, "a", tid), True)
        self.assertEqual(s.deposit(11, "a", 0), 1700)
        self.assertEqual(s.top_activity(12, 3), ["a(1700)", "c(400)"])

    def test_level_4_case_06_transfer_between_the_two_cancelled(self):
        s = self._two_accounts()
        t1 = s.transfer(5, "a", "b", 100)
        t2 = s.transfer(6, "b", "a", 50)
        s.merge_accounts(7, "a", "b")
        self.assertIs(s.accept_transfer(8, "a", t1), False)
        self.assertIs(s.accept_transfer(9, "a", t2), False)
        self.assertEqual(s.deposit(10, "a", 0), 1500)        # nothing lost, nothing doubled
        self.assertEqual(s.top_activity(11, 1), ["a(1500)"])

    def test_level_4_case_07_balance_history(self):
        s = self.system
        s.create_account(10, "a")
        s.deposit(20, "a", 100)
        s.pay(30, "a", 40)
        s.pay(40, "a", 999)                                  # failed: no change
        self.assertIsNone(s.get_balance(50, "a", 9))          # before creation
        self.assertEqual(s.get_balance(51, "a", 10), 0)       # created at 10
        self.assertEqual(s.get_balance(52, "a", 25), 100)
        self.assertEqual(s.get_balance(53, "a", 30), 60)      # inclusive: after the op at time_at
        self.assertEqual(s.get_balance(54, "a", 45), 60)
        self.assertIsNone(s.get_balance(55, "ghost", 45))

    def test_level_4_case_08_merged_account_keeps_its_past(self):
        s = self._two_accounts()
        s.pay(5, "b", 100)
        s.merge_accounts(6, "a", "b")
        self.assertEqual(s.get_balance(7, "b", 4), 500)
        self.assertEqual(s.get_balance(8, "b", 5), 400)
        self.assertIsNone(s.get_balance(9, "b", 6))           # gone from the merge on
        self.assertEqual(s.get_balance(10, "a", 5), 1000)     # a's own past is not rewritten
        self.assertEqual(s.get_balance(11, "a", 6), 1400)

    def test_level_4_case_09_expired_refund_dated_at_expiry(self):
        s = self._two_accounts()
        s.transfer(5, "a", "b", 400)
        s.deposit(5 + 2 * DAY, "b", 0)                        # first query after the expiry
        self.assertEqual(s.get_balance(5 + 2 * DAY + 1, "a", 5), 600)
        self.assertEqual(s.get_balance(5 + 2 * DAY + 2, "a", 5 + DAY), 600)       # last valid ms: still held
        self.assertEqual(s.get_balance(5 + 2 * DAY + 3, "a", 5 + DAY + 1), 1000)  # refunded from t + 1 day + 1

    def test_level_4_case_10_recreated_id_has_a_gap(self):
        s = self._two_accounts()
        s.merge_accounts(5, "a", "b")
        s.create_account(7, "b")
        s.deposit(8, "b", 30)
        self.assertEqual(s.get_balance(9, "b", 4), 500)       # first life
        self.assertIsNone(s.get_balance(10, "b", 6))          # between lives
        self.assertEqual(s.get_balance(11, "b", 7), 0)
        self.assertEqual(s.get_balance(12, "b", 8), 30)

    def test_level_4_case_11_perf_within_time_limit(self):
        s = self.system
        start = time.perf_counter()
        ts = 0
        for i in range(300):
            ts += 1
            s.create_account(ts, f"acc{i}")
        for i in range(6000):
            ts += 1
            s.deposit(ts, f"acc{i % 300}", 5)
        for i in range(0, 300, 2):
            ts += 1
            s.merge_accounts(ts, f"acc{i}", f"acc{i + 1}")
        for i in range(3000):
            ts += 1
            s.get_balance(ts, f"acc{i % 300}", i * 2)
        self.assertLess(time.perf_counter() - start, 0.4)


if __name__ == "__main__":
    unittest.main()

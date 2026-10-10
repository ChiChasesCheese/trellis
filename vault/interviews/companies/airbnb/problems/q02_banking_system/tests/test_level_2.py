"""Level 2 — top_activity (reconstructed). Case 01 is the GitHub statement example; the rest are ours."""
import importlib
import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Impl = importlib.import_module(os.environ.get("IMPL", "solution")).BankingSystemImpl


class Level2Tests(unittest.TestCase):
    def setUp(self):
        self.system = Impl()

    def test_level_2_case_01_statement_example(self):
        s = self.system
        s.create_account(1, "account1")
        s.create_account(2, "account2")
        s.deposit(3, "account1", 2000)
        s.deposit(4, "account2", 3000)
        self.assertEqual(s.top_activity(5, 2), ["account2(3000)", "account1(2000)"])

    def test_level_2_case_02_payments_count_too(self):
        s = self.system
        s.create_account(1, "a")
        s.create_account(2, "b")
        s.deposit(3, "a", 1000)
        s.pay(4, "a", 900)          # a: 1000 + 900 = 1900, balance 100
        s.deposit(5, "b", 1500)
        self.assertEqual(s.top_activity(6, 2), ["a(1900)", "b(1500)"])

    def test_level_2_case_03_failed_operations_do_not_count(self):
        s = self.system
        s.create_account(1, "a")
        s.deposit(2, "a", 100)
        s.pay(3, "a", 1000)         # insufficient: not a transaction
        s.deposit(4, "ghost", 500)
        self.assertEqual(s.top_activity(5, 5), ["a(100)"])

    def test_level_2_case_04_ties_alphabetical(self):
        s = self.system
        for i, name in enumerate(["c", "a", "b"]):
            s.create_account(i + 1, name)
            s.deposit(i + 10, name, 500)
        self.assertEqual(s.top_activity(20, 3), ["a(500)", "b(500)", "c(500)"])

    def test_level_2_case_05_n_larger_than_accounts_and_zero_activity(self):
        s = self.system
        s.create_account(1, "b")
        s.create_account(2, "a")
        self.assertEqual(s.top_activity(3, 10), ["a(0)", "b(0)"])

    def test_level_2_case_06_truncates_to_n(self):
        s = self.system
        for i in range(5):
            s.create_account(i + 1, f"acc{i}")
            s.deposit(i + 10, f"acc{i}", (i + 1) * 100)
        self.assertEqual(s.top_activity(20, 2), ["acc4(500)", "acc3(400)"])

    def test_level_2_case_07_numeric_not_string_order(self):
        # Sorting the formatted strings, or by str(total), puts "900" above "1000".
        s = self.system
        s.create_account(1, "a")
        s.create_account(2, "b")
        s.deposit(3, "a", 900)
        s.deposit(4, "b", 1000)
        self.assertEqual(s.top_activity(5, 2), ["b(1000)", "a(900)"])

    def test_level_2_case_08_perf_within_time_limit(self):
        s = self.system
        start = time.perf_counter()
        ts = 0
        for i in range(2000):
            ts += 1
            s.create_account(ts, f"acc{i}")
        for i in range(10000):
            ts += 1
            s.deposit(ts, f"acc{i % 2000}", i)
        for _ in range(100):
            ts += 1
            s.top_activity(ts, 10)
        self.assertLess(time.perf_counter() - start, 0.4)


if __name__ == "__main__":
    unittest.main()

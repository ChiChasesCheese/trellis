"""Level 1 — 10 tests, like the real level_1_tests.py. Cases 01-03 are copied from the assessment photos
(case 03 is cut off after its fourth line; the rest of it is ours); case 04 is the statement example; 05-10 are ours."""
import importlib
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Impl = importlib.import_module(os.environ.get("IMPL", "solution")).BankingSystemImpl


class Level1Tests(unittest.TestCase):
    def setUp(self):
        self.system = Impl()

    # ---- from the photos ------------------------------------------------------------------

    def test_level_1_case_01_basic_create(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))

    def test_level_1_case_02_basic_create_and_deposit(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 2500), 2500)
        self.assertEqual(self.system.deposit(4, 'account1', 500), 3000)
        self.assertEqual(self.system.deposit(5, 'account2', 1000), 1000)

    def test_level_1_case_03_basic_create_deposit_and_pay(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 2000), 2000)
        self.assertEqual(self.system.deposit(4, 'account2', 1000), 1000)
        # cut off in the photo from here on
        self.assertEqual(self.system.pay(5, 'account1', 500), 1500)
        self.assertEqual(self.system.pay(6, 'account2', 1000), 0)

    def test_level_1_case_04_statement_example(self):
        s = self.system
        self.assertIs(s.create_account(1, "account1"), True)
        self.assertIs(s.create_account(2, "account1"), False)
        self.assertIs(s.create_account(3, "account2"), True)
        self.assertIsNone(s.deposit(4, "non-existing", 2700))
        self.assertEqual(s.deposit(5, "account1", 2700), 2700)
        self.assertIsNone(s.pay(6, "non-existing", 2700))
        self.assertIsNone(s.pay(7, "account1", 2701))
        self.assertEqual(s.pay(8, "account1", 200), 2500)

    # ---- ours -------------------------------------------------------------------------------

    def test_level_1_case_05_duplicate_create_keeps_balance(self):
        # Re-creating must not reset the existing account to 0.
        self.system.create_account(1, "a")
        self.system.deposit(2, "a", 100)
        self.assertIs(self.system.create_account(3, "a"), False)
        self.assertEqual(self.system.deposit(4, "a", 1), 101)

    def test_level_1_case_06_pay_exact_balance_to_zero(self):
        self.system.create_account(1, "a")
        self.system.deposit(2, "a", 300)
        self.assertEqual(self.system.pay(3, "a", 300), 0)   # 0 is a balance, not "failed"
        self.assertIsNone(self.system.pay(4, "a", 1))

    def test_level_1_case_07_failed_pay_changes_nothing(self):
        self.system.create_account(1, "a")
        self.system.deposit(2, "a", 100)
        self.assertIsNone(self.system.pay(3, "a", 101))
        self.assertEqual(self.system.pay(4, "a", 100), 0)

    def test_level_1_case_08_accounts_are_independent(self):
        self.system.create_account(1, "a")
        self.system.create_account(2, "b")
        self.system.deposit(3, "a", 50)
        self.assertIsNone(self.system.pay(4, "b", 10))
        self.assertEqual(self.system.deposit(5, "b", 10), 10)
        self.assertEqual(self.system.pay(6, "a", 50), 0)

    def test_level_1_case_09_deposit_and_pay_on_missing_account(self):
        self.assertIsNone(self.system.deposit(1, "ghost", 10))
        self.assertIsNone(self.system.pay(2, "ghost", 0))
        self.assertIs(self.system.create_account(3, "ghost"), True)
        self.assertEqual(self.system.deposit(4, "ghost", 10), 10)

    def test_level_1_case_10_zero_amounts(self):
        self.system.create_account(1, "a")
        self.assertEqual(self.system.deposit(2, "a", 0), 0)
        self.assertEqual(self.system.pay(3, "a", 0), 0)


if __name__ == "__main__":
    unittest.main()

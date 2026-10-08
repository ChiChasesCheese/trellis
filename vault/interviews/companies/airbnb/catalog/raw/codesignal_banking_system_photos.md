# Raw: CodeSignal "Banking System": phone photos of a CodeSignal assessment

- **Source:** 7 phone photos of a CodeSignal ICF screen, found online and supplied by Chi on 2026-10-08.
  The photos are not committed: the repo is public, and one of them shows a driver's licence on the desk next to the screen.
- **Company:** the photos do not name a company. The Airbnb filing comes from Chi. Same template and format as q01
  (`codesignal_parcel_tracking_photos.md`).
- **Confidence:** Level 1 **high** (spec, interface, example and test cases 01–03 read off the screen). Levels 2–4:
  one-line summaries **high** (verbatim); methods and semantics **medium/low**, taken from GitHub reconstructions (below).

## Environment visible in the photos

- Page title `Filesystem with Unit Tests` (the CodeSignal project template, not the problem). "Question 1 of 1".
- `Python 3 / unittest`, `[execution time limit] 3 seconds`, `[memory limit] 6g`; every test carries `@timeout(0.4)`.
- Files: `tests/level_1_tests.py` (locked), `tests/sandbox_tests.py`, `banking_system.py` (locked ABC),
  `banking_system_impl.py` (editable), `main.sh`, `run_single_test.sh`.
- `banking_system_impl.py` as shipped:
  ```python
  from banking_system import BankingSystem


  class BankingSystemImpl(BankingSystem):

      def __init__(self):
          # TODO: implement
          pass

      # TODO: implement interface methods here
  ```
- `level_1_tests.py` docstring: "The test suit below includes 10 tests for Level 1. All have the same score. You are not
  allowed to modify this file, but feel free to read the source code to better understand what is happening in every
  specific case." `setUp` is decorated `@classmethod` and sets `cls.system = BankingSystemImpl()`.
- `sandbox_tests.py` docstring: a playground; its results "do not affect the final score (unless the project fails to
  build)". "Do not reuse the name of an existing unit test. If a sandbox test has the same name as a scored test, that
  scored test will not be counted and a full score is impossible."

## Verbatim text

> **Instructions.** Your task is to implement a simplified version of a banking system. All operations that should be
> supported are listed below.
>
> Solving this task consists of several levels. Subsequent levels are opened when the current level is correctly
> solved. You always have access to the data for the current and all previous levels.
>
> You are not required to provide the most efficient implementation. Any code that passes the unit tests is sufficient.
>
> You can execute a single test case by running the following command in the terminal:
> `bash run_single_test.sh "<test_case_name>"`.
>
> **Requirements.** Your task is to implement a simplified version of a banking system. Plan your design according to
> the level specifications below:
>
> - Level 1: The banking system should support creating new accounts and depositing money into and withdrawing/paying
>   money from accounts.
> - Level 2: The banking system should support ranking accounts based on the total value of transactions.
> - Level 3: The banking system should support initiating transfers that the target account must accept, and checking
>   the status of those transfers.
> - Level 4: The banking system should support merging two accounts while retaining the balances and transaction
>   histories of the original accounts.
>
> To move to the next level, you should pass all the tests at the current level.
>
> **Note.** All queries will have a `timestamp` parameter — a stringified timestamp in milliseconds. It is guaranteed
> that all … *(cut off in the photo; the usual CodeSignal wording is "timestamps are unique and are in a strictly
> increasing order")*

> **Level 1.** The banking system should support creating new accounts and depositing money into and
> withdrawing/paying money from accounts.
>
> - `create_account(self, timestamp: int, account_id: str) -> bool` — should create a new account with the given
>   `account_id` if it doesn't already exist. Returns `True` if the account was successfully created or `False` if an
>   account with `account_id` already exists.
> - `deposit(self, timestamp: int, account_id: str, amount: int) -> int | None` — should deposit the given `amount` of
>   money to the specified account `account_id`. Returns the total amount of money in the account (balance) after
>   processing the query. If the specified account does not exist, should return `None`.
> - `pay(self, timestamp: int, account_id: str, amount: int) -> int | None` — should withdraw the given `amount` of
>   money from the specified account. Returns the amount of money in the account (balance) after processing the
>   query. If the specified account does not exist, or if the account has insufficient funds to perform the
>   withdrawal, should return `None`.

Level 1 example (verbatim):

| Query | Explanation |
|---|---|
| `create_account(1, "account1")` | returns `True` |
| `create_account(2, "account1")` | returns `False`; an account with this identifier already exists |
| `create_account(3, "account2")` | returns `True` |
| `deposit(4, "non-existing", 2700)` | returns `None`; an account with this identifier does not exist |
| `deposit(5, "account1", 2700)` | returns `2700` |
| `pay(6, "non-existing", 2700)` | returns `None`; an account with this identifier does not exist |
| `pay(7, "account1", 2701)` | returns `None`; this account has insufficient funds |
| `pay(8, "account1", 200)` | returns `2500` |

Level 1 tests visible (`level_1_tests.py`, lines 28–46):

```python
@timeout(0.4)
def test_level_1_case_01_basic_create(self):
    self.assertTrue(self.system.create_account(1, 'account1'))
    self.assertTrue(self.system.create_account(2, 'account2'))

@timeout(0.4)
def test_level_1_case_02_basic_create_and_deposit(self):
    self.assertTrue(self.system.create_account(1, 'account1'))
    self.assertTrue(self.system.create_account(2, 'account2'))
    self.assertEqual(self.system.deposit(3, 'account1', 2500), 2500)
    self.assertEqual(self.system.deposit(4, 'account1', 500), 3000)
    self.assertEqual(self.system.deposit(5, 'account2', 1000), 1000)

@timeout(0.4)
def test_level_1_case_03_basic_create_deposit_and_pay(self):
    self.assertTrue(self.system.create_account(1, 'account1'))
    self.assertTrue(self.system.create_account(2, 'account2'))
    self.assertEqual(self.system.deposit(3, 'account1', 2000), 2000)
    self.assertEqual(self.system.deposit(4, 'account2', 1000), 1000)
    # ... cut off at line 46
```

## Levels 2–4: GitHub reconstructions (fetched 2026-10-08)

| Source | Confidence | What it gives |
|---|---|---|
| https://github.com/FazeelUsmani/Industry-Problems/tree/main/simplified-banking-system | medium | Four level titles match the photo summaries one-to-one. L2 `top_activity(timestamp, n)`: "sum of all successful deposits and withdrawals", ties alphabetical, format `"<id>(<value>)"`. L3 `transfer(timestamp, source, target, amount) -> "transferX" \| None`, `accept_transfer(timestamp, account_id, transfer_id) -> bool`, expiry 24 h = 86 400 000 ms, expired funds return to source. L4 `merge_accounts(timestamp, account_id_1, account_id_2)`: cancels outgoing transfers of account 2, redirects incoming to account 1, adds balances; `get_balance(timestamp, account_id, time_at)`; example `get_balance(7, "account2", 6) → None` after the merge. Its solution counts accepted transfers in both accounts' activity and treats `ts == start + 1 day` as still acceptable. |
| https://github.com/danielrezende3/codesignal/blob/main/banking_system/.levels/stubs_full.py | low | Same L1/L3/L4 signatures; L2 is `top_spenders(timestamp, n)` (outgoing only) — a different variant of the same problem. |
| https://github.com/DrustZ/ai_interview_prep_2026/blob/main/online_resource/drills/09_banking_system.py | low | An AI-written drill: expiry at `ts >= expires_at` (half-open), merged account has `ended_at`, `get_balance` → `None` before creation or after merge. |

The photos say "ranking accounts based on the **total value of transactions**", which matches `top_activity`, not
`top_spenders`. Where the sources disagree, `problem.md` labels the choice **(reconstructed)**.

## Real Level 3 tests (second batch, 2026-10-08)

Photos of the real `tests/level_3_tests.py` (locked) and of a Unit Tests run. Test names seen: `case_02_basic_transfer_expiration`,
`case_03_basic_transfer_and_accept_transfer`, `case_04_multiple_transfers_and_acceptances`, `case_05_transfer_edge_cases`,
`case_10_all_operations_3`. Confirms `transfer` / `accept_transfer` names, `'transfer<k>'` ids, and the 24 h boundary:

```python
def test_level_3_case_02_basic_transfer_expiration(self):
    self.assertTrue(self.system.create_account(1, 'account1'))
    self.assertTrue(self.system.create_account(2, 'account2'))
    self.assertEqual(self.system.deposit(3, 'account1', 2000), 2000)
    self.assertEqual(self.system.transfer(4, 'account1', 'account2', 1000), 'transfer1')
    self.assertEqual(self.system.deposit(86400004, 'account1', 100), 1100)   # t + 1 day exactly: NOT refunded yet
    self.assertEqual(self.system.deposit(86400005, 'account2', 100), 100)

def test_level_3_case_03_basic_transfer_and_accept_transfer(self):
    ...create account1, account2; deposit(3, 'account1', 2000) == 2000
    self.assertEqual(self.system.transfer(4, 'account1', 'account2', 1000), 'transfer1')
    self.assertTrue(self.system.accept_transfer(5, 'account2', 'transfer1'))
    self.assertEqual(self.system.deposit(6, 'account1', 100), 1100)
    self.assertEqual(self.system.deposit(7, 'account2', 100), 1100)

def test_level_3_case_04_multiple_transfers_and_acceptances(self):
    ...create account1..3; deposit(4, 'account1', 2000) == 2000
    transfer(5, 'account1', 'account2', 500) == 'transfer1'; transfer(6, 'account1', 'account3', 500) == 'transfer2'
    deposit(86400002, 'account1', 100) == 1100; deposit(86400003, 'account2', 100) == 100; deposit(86400004, 'account3', 100) == 100
    self.assertTrue(self.system.accept_transfer(86400005, 'account2', 'transfer1'))   # made at 5: t + 1 day exactly, still valid
    self.assertTrue(self.system.accept_transfer(86400006, 'account3', 'transfer2'))
    deposit(86400007, 'account1', 100) == 1200; deposit(86400008, 'account2', 100) == 700; deposit(86400009, 'account3', 100) == 700
```

`case_05_transfer_edge_cases` (partly covered by a phone overlay): transfers from / to `'non-existing'`, amount 2001 > balance,
`account1 → account1`, all `None`; then `transfer(7, 'account1', 'account2', 1000) == 'transfer1'`.
The run screen showed `2100 != 1100` on case 02 and `False is not true` on case 04 for an implementation expiring at `ts >= t + 1 day`.

# q02 · Banking System (CodeSignal ICF, 4 levels)

- **Format:** CodeSignal Industry Coding Framework (ICF/ICA), same template as q01: one project, 4 levels unlocked in
  sequence, Python 3 + `unittest`, 10 tests in Level 1; the page says 3 s / 6g, but every test carries `@timeout(0.4)`.
- **Source:** phone photos of a CodeSignal screen → `../../catalog/raw/codesignal_banking_system_photos.md`.
  Level 1 is verbatim (high confidence). Levels 2–4: the one-line summaries are verbatim; methods and semantics are
  **(reconstructed)** from GitHub versions of the same problem (medium/low confidence).
- **Company:** Airbnb per Chi; the photos name no company.

## Files

| File | Role |
|---|---|
| `banking_system.py` | the locked ABC interface (L1 verbatim, L2–4 reconstructed, default implementations) |
| `starter_template.py` → `starter.py` | your file (CodeSignal's `banking_system_impl.py`) |
| `solution_level1.py` … `solution_level4.py` | the standard answer after each level; each is the previous one plus the smallest change |
| `solution.py` | reference solution (= `solution_level4.py`) |
| `tests/test_level_{1..4}.py` | 42 `unittest` cases (L1 10, L2 8, L3 13 incl. 3 copied from the real file, L4 11); `IMPL=starter` runs them against your file |
| `mutation_check.py` | 16 one-bug mutants of `solution.py`; every one must fail a test |
| `run_single_test.sh` | `bash run_single_test.sh case_03` |

## Requirements (verbatim)

- Level 1: The banking system should support creating new accounts and depositing money into and withdrawing/paying
  money from accounts.
- Level 2: The banking system should support ranking accounts based on the total value of transactions.
- Level 3: The banking system should support initiating transfers that the target account must accept, and checking
  the status of those transfers.
- Level 4: The banking system should support merging two accounts while retaining the balances and transaction
  histories of the original accounts.

All queries carry a `timestamp` in milliseconds; timestamps are unique and strictly increasing *(the guarantee is cut
off in the photo; this is the standard CodeSignal wording)*.

## Level 1 — accounts, deposit, pay (verbatim)

- `create_account(timestamp, account_id) -> bool` — create the account if it does not exist. `True` on success, `False`
  if `account_id` already exists.
- `deposit(timestamp, account_id, amount) -> int | None` — add `amount`; return the balance after the query; `None` if the
  account does not exist.
- `pay(timestamp, account_id, amount) -> int | None` — withdraw `amount`; return the balance after the query; `None` if the
  account does not exist or has insufficient funds.

| Query | Result |
|---|---|
| `create_account(1, "account1")` | `True` |
| `create_account(2, "account1")` | `False` — already exists |
| `create_account(3, "account2")` | `True` |
| `deposit(4, "non-existing", 2700)` | `None` — no such account |
| `deposit(5, "account1", 2700)` | `2700` |
| `pay(6, "non-existing", 2700)` | `None` — no such account |
| `pay(7, "account1", 2701)` | `None` — insufficient funds |
| `pay(8, "account1", 200)` | `2500` |

## Level 2 — ranking by activity (reconstructed)

- `top_activity(timestamp, n) -> list[str]` — the top `n` accounts by total value of transactions, as
  `"<account_id>(<total>)"`, descending by total, ties by `account_id` ascending; fewer than `n` accounts → all of them.
  Total = sum of successful deposits and payments (from Level 3 also accepted transfers, counted on both sides).
  Failed operations do not count.

Example: create `account1`, `account2`; deposit 2000 / 3000 → `top_activity(5, 2) == ["account2(3000)", "account1(2000)"]`.

Variant seen on GitHub: `top_spenders(timestamp, n)` ranks by **outgoing** money only (payments + accepted outgoing
transfers). The photos say "total value of transactions", so this kit follows `top_activity`. If the real Level 2 says
"outgoing", only the two `+=` lines in `deposit` and the target side of `accept_transfer` change.

## Level 3 — transfers that must be accepted (reconstructed)

- `transfer(timestamp, source_account_id, target_account_id, amount) -> str | None` — withdraw `amount` from the source
  now and hold it. Returns `"transfer<k>"`, `k` counting successful transfers from 1. `None` if source == target, either
  account does not exist, or the source has insufficient funds.
- `accept_transfer(timestamp, account_id, transfer_id) -> bool` — credit the target. `False` if the transfer does not
  exist, was already accepted, has expired, or `account_id` is not its target.
- A transfer expires 24 h = `86400000` ms after it was initiated. **Boundary confirmed by the real tests** (cases 02–04
  of the real `level_3_tests.py`, photographed 2026-10-08): it is still pending and acceptable at exactly
  `t + 86400000`; from `t + 86400001` on, the held money is back in the source account (visible to every later query).
  Our first reconstruction used the half-open window `[t, t + 86400000)` and was wrong by one millisecond; the
  CodeSignal convention for TTLs elsewhere (q01), which is exactly why it is a trap here.

Example: create both, deposit 2000 to `account1`; `transfer(4, "account1", "account2", 1000) == "transfer1"`;
`accept_transfer(5, "account2", "transfer1") is True`.

The summary also says "checking the status of those transfers". No reconstruction has a status method; if the real
Level 3 has one (e.g. `get_transfer_status`), keep the accepted / expired transfers instead of deleting them.

## Level 4 — merge and historical balance (reconstructed)

- `merge_accounts(timestamp, account_id_1, account_id_2) -> bool` — merge account 2 into account 1. `False` if the ids are
  equal or either account does not exist. Pending transfers **from** account 2, and pending transfers between the two
  accounts, are cancelled and refunded; pending transfers **to** account 2 are redirected to account 1. Balance and
  activity of account 2 are added to account 1; account 2 stops existing (its id can be created again).
- `get_balance(timestamp, account_id, time_at) -> int | None` — the balance after every operation with timestamp
  `<= time_at`; `None` if the account did not exist at `time_at` (not yet created, or merged away). The past of each
  original account is kept as it was: `get_balance(·, account_id_1, before_merge)` is account 1's own balance then.

Example: create both, deposit 1000 each, `merge_accounts(5, "account1", "account2") is True`;
`get_balance(6, "account1", 3) == 1000`; `get_balance(7, "account2", 6) is None`.

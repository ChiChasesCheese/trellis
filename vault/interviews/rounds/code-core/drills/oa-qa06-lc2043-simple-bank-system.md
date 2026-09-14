---
nodes: [model.state-machine, rules.money]
tags: [stripe-oa, qa06, leetcode]
---
# Drill: a validated bank class, then a reversible log, then platform lending

Forty-five minutes. This is LeetCode 2043, Simple Bank System, extended into
a three-part ledger design. Build a `Bank` class over 1-indexed accounts with
`transfer(a, b, money)`, `deposit(a, money)`, and `withdraw(a, money)`, each
returning whether the call was valid and applying its effect only when it
was — an invalid call must leave every balance untouched. Part 1 is the LC
class as stated. Part 2 adds a transaction log: every call, valid or not,
appends a record with a sequential id, and `reverse(txn_id)` undoes a prior
successful, not-yet-reversed, non-reverse record if the undo itself can be
funded. Part 3 adds a platform `reserve`: an overdrawing withdraw or transfer
may borrow exactly the shortfall from the reserve, tracking per-account debt
that is auto-repaid out of later incoming money before it reaches the
balance.

**Constraints to state and honor**
- Accounts are 1-indexed; account 0, account n+1, and negative ids are all
  invalid, and an invalid transfer must not debit a valid source.
- Balances and amounts run up to 10^12 with up to 10^4 calls — use exact
  integers, no floats, no overflow concerns in Python.
- Withdrawing exactly the balance is valid; one unit more is not; amount 0
  is valid; `a == b` transfers are valid when funded.
- Part 2: a reversal fails if the record doesn't exist, wasn't `ok`, is
  itself a reverse, has already been reversed, or the undo can't be funded;
  reversals never borrow from the reserve even in Part 3.
- Part 3: the platform lends only the exact shortfall when the reserve
  covers it (rejecting the whole operation otherwise); incoming money repays
  debt first, capped at the debt amount, before crediting the balance.

**Grading points**
- Validate fully before mutating anything — a transfer checks both accounts
  and the source balance before touching either side, so a failed transfer
  changes nothing.
- Every call gets logged uniformly, including failed calls and `reverse`
  itself, with monotonically assigned ids — say out loud why failed calls
  still need a log entry (later reversals reference them by id).
- The reversal rule per operation kind is asymmetric: undoing a deposit
  debits, undoing a withdraw credits, undoing a transfer moves the money
  back — and each of those can itself fail for insufficient funds.
- Platform lending needs two hooks on the money-movement primitives: a debit
  path that can create debt when the reserve allows it, and a credit path
  that repays debt before touching the balance; `max_outstanding` tracks the
  peak of total debt across all steps, not just the final value.
- Boundary discipline: shortfall exactly equal to the reserve is fundable;
  repayment never exceeds the debt; `reserve=0` must degenerate exactly to
  Part 1 behavior.
- Edge cases: reversing an already-reversed, failed, or reverse-kind record;
  an unfundable reversal leaving state untouched; 10^12-scale balances
  summed without precision loss.

**Source**
- `vault/interviews/companies/stripe/problems/qA06_lc2043_simple_bank_system/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/qA06_lc2043_simple_bank_system.md`
- `vault/interviews/companies/stripe/problems/qA06_lc2043_simple_bank_system/problem.md`, `vault/interviews/companies/stripe/problems/qA06_lc2043_simple_bank_system/REPORT.md`
- `vault/interviews/companies/stripe/study/10-solutions/qA06_lc2043_simple_bank_system.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):

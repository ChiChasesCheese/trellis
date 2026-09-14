---
nodes: [rules.money, algorithms.settlement, transfer.stripe-oa]
tags: [stripe-oa, q13]
---
# Drill: a cents-exact ledger with overdraft rejection and a platform lender

Sixty minutes, stdin to stdout. Transactions arrive one per line — `credit`, `debit`, and (Part
3) `transfer` — against a per-user balance ledger, amounts given as decimal strings that must be
parsed into integer cents and never touched as floats. Part 1 just applies every line and prints
final non-zero balances. Part 2 rejects any debit that would take a balance below zero. Part 3
introduces a special `platform` account that covers a shortfall out of its own funds when a
non-platform debit or transfer would overdraw, gets repaid automatically out of that user's next
incoming money, and must report the peak amount it ever had outstanding at once.

**Constraints to state and honor**
- First line `PART n`; `txn_id,user_id,credit,amount` / `txn_id,user_id,debit,amount` / (Part 3)
  `txn_id,from_user,transfer,to_user,amount`; amounts are non-negative decimal strings with up to
  two decimals; up to 2·10^5 lines.
- Output: one line per user with non-zero final balance as `user_id balance` (`x.xx`, sorted by
  plain string order), then (Parts 2–3) `REJECTED: id1,id2,…` or `REJECTED: NONE`, then (Part 3)
  `MAX_RESERVE: x.xx`.
- Debit rejection is strict: `balance − amount < 0` rejects; landing exactly on `0.00` is
  accepted; a debit on a never-seen user is rejected.
- The platform lends exactly the shortfall only if it can cover the whole thing (no partial
  loans), never borrows itself, and a user's loan is repaid automatically — capped at the loan —
  whenever that user next receives money, including as the receiving side of a transfer.

**Grading points**
- Money goes through `Decimal` or manual scaling into integer cents on the way in, and a small
  `fmt(cents)` helper on the way out — never float arithmetic on amounts.
- `can_debit` as one shared predicate reused by Part 2's plain rejection and Part 3's
  shortfall-then-borrow path, so the strict-vs-lenient overdraft rule lives in exactly one place.
- Repayment on credit is explicit and separate from the balance update: `repay = min(loan,
  incoming)` goes to the platform first, and only the remainder lands in the user's own balance.
- `MAX_RESERVE` is a running peak over total outstanding loans measured right after a loan is
  issued — and, within a single transfer, *before* the receiving side's automatic repayment —
  not the final total.
- Zero-balance accounts are omitted from output even when they had activity; `REJECTED: NONE` and
  `MAX_RESERVE: 0.00` still print on an otherwise empty run.
- A rejected transfer must leave both sides completely untouched, and the platform's own
  debits/transfers can never borrow.

**Source**
- `vault/interviews/companies/stripe/problems/q13_account_balance_ledger/problem.md`, `vault/interviews/companies/stripe/problems/q13_account_balance_ledger/REPORT.md`, `vault/interviews/companies/stripe/problems/q13_account_balance_ledger/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q13_account_balance_ledger.md`, `vault/interviews/companies/stripe/study/10-solutions/q13_account_balance_ledger.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):

# q13 Account Balance Ledger — report

## Summary
A credit/debit ledger processed strictly in order — Stripe's balance-transaction model reduced to a
dict of cents. Part 1 is parsing + exact money formatting, Part 2 adds the strict overdraft rejection,
Part 3 adds transfers and a Connect-style `platform` that lends the shortfall, is repaid automatically
from the borrower's next incoming money, and must report the peak amount lent (`MAX_RESERVE`).

## Sources & confidence
medium — 1point3acres 题库 `account-balance-manager` (OA Easy, last asked 2026-05-12), linkjob intern
VO 3-part spec, prachub "Build an Account Transfer Ledger" (`platform_id`, `max_reserve`), dev.to /
programhelp `user event amount` logs, GitHub Shivam5022 OA mention. The three-part structure is
consistent across sources; the transfer line shape (`txn,from,transfer,to,amount`) and the exact
`REJECTED:` / `MAX_RESERVE:` output lines are reconstructed.

## Approach by part
1. `to_cents` via `Decimal(...).quantize(0.01, ROUND_HALF_UP) * 100` (never float); `bal[user] += ±cents`;
   render non-zero balances sorted by plain string order with `fmt` (sign + `//100` + `%100:02d`).
2. `can_debit`: `shortfall = amount − balance`; `shortfall > 0` ⇒ reject (strict: landing on 0 is fine).
   Rejected ids kept in input order; `REJECTED: NONE` when empty.
3. Same `can_debit`: a non-platform shortfall is lent if `platform ≥ shortfall` (≥, so lending the
   whole platform balance is allowed). `credit()` first repays `min(loan, incoming)` to the platform.
   `max_reserve` is updated right after each loan (before the receiving side of a transfer repays).
   Transfers = `debit` then `credit`; a rejected transfer touches nothing.

## Pitfalls hidden tests target
- float parsing (`0.10 + 0.20`), `-3.5` vs `-3.50`, sign placement for negatives
- zero-balance accounts printed; string vs numeric sort (`user10` < `user2`)
- `balance − amount < 0` strict vs `<=` (exact-zero debit must pass); unknown user debit rejected
- Part 3: borrowing more than the shortfall, partial loans when the platform is short, letting the
  platform borrow, repaying more than the loan, measuring the reserve at the end instead of the peak,
  counting the reserve after the receiver's repayment (14 vs 10 in the transfer test)

## Complexity & measured cost
O(n + u log u). Measured: 0.30s, 48 MB (200k lines, 5k users, 20% transfers; in-pytest 0.47 s;
budget 2 s / 256 MB).

## Test inventory
22 tests — part1: 7 · part2: 5 · part3: 10; edge 11 · fmt 3 · io 2 · perf 1.

## Skills exercised
S02 CSV parsing · S03 per-account records · S05 strict overdraft boundary · S06 integer cents +
formatting · S08 sorted output · S09 exact output lines · S10 ordered events · S17 ledger balances ·
S19 incremental design

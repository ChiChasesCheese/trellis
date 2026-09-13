# q10 Payment Intent Commands — report

## Summary
Replay a log of PaymentIntent API commands (`INIT / CREATE / ATTEMPT / SUCCEED`, then
`UPDATE`, then `FAIL / REFUND`, then timestamps with a refund window) against an in-memory
ledger and print each merchant's balance. It is the PaymentIntent state machine
`requires_action → processing → succeeded` with money moving only on SUCCEED and refunds
applied once. Nearly every hidden test is an invalid command that must be silently ignored.

## Sources & confidence
high — 5 independent sources: csoahelp 2024-12-15 (version A, 3 parts — primary), csoahelp
2024-12-11 (version B "Transaction Intent Management System"), csoahelp 2025-04-22 (version C:
REFUND + window, 4 parts), 1point3acres threads 1091979 / 1101931 / 1085478 / 1099687,
medium @azn7u1 (INIT/CREATE sample); https://docs.stripe.com/refunds for refund-once semantics.

## Approach by part
A `Ledger` with `balances`, `payments: id -> Payment(merchant, amount, state, refunded,
t_create)` and `limits`. Dispatch checks the command word against the part's command set and
an `ARITY` table; malformed numbers make the command a no-op (`_int` → `None`).
1. Duplicate `INIT` never resets; `CREATE` rejects duplicate id / unknown merchant / negative
   amount (0 ok); `ATTEMPT` and `SUCCEED` are guarded transitions; the credit happens on SUCCEED.
2. `UPDATE` only in `REQUIRES_ACTION`, non-negative.
3. `FAIL`: `PROCESSING → REQUIRES_ACTION` (re-editable); `REFUND` only when `COMPLETED` and
   not yet refunded, debits the credited amount.
4. Timestamped lines; `INIT m bal [limit]` (`None` = always, `0` = never, else
   `t_refund − t_create <= limit`, inclusive). Version C: `CREATE` completes and credits
   immediately (`immediate_credit=True`); `part4(lines, immediate_credit=False)` keeps the full
   machine for version B. Output `merchant balance` sorted as plain strings.

## Pitfalls hidden tests target
- second `INIT` must not reset; `CREATE` duplicate / unknown merchant / negative → ignored
- `SUCCEED` without `ATTEMPT`, twice, or `ATTEMPT` on `COMPLETED` → ignored
- `UPDATE` after `ATTEMPT` ignored, but valid again after `FAIL`; SUCCEED credits the updated amount
- `REFUND` twice / of a non-completed payment ignored; refund debits the credited amount;
  balances may go negative; zero balances still printed; `m10` < `m2` string order
- Part 4 window: `== limit` allowed, `+1` refused, limit `0` never, absent always, a refused
  refund can be retried; `CREATE` credits immediately without SUCCEED
- unknown words / wrong arity / non-integer numbers never crash

## Complexity & measured cost
O(n) over commands plus O(m log m) for the final sort. 2,000 merchants + 198k commands
(50k payments): ~0.17 s, ~53 MB RSS (budget 2 s / 256 MB).
Measured: 0.170s, 53 MB

## Test inventory
24 tests — part1: 8 · part2: 4 · part3: 5 · part4: 7; edge 14 · fmt 1 · perf 1 · io 1.
`IMPL=starter`: 24 fail / 0 pass.

## Skills exercised
S02 parsing · S03 records + dicts keyed by id · S10 state machine with reversals ·
S11 idempotency (INIT/CREATE/REFUND) · S12 time windows · S18 validation & error paths ·
S19 incremental design

---
nodes: [model.idempotency, chrono.intervals, transfer.stripe-oa]
tags: [stripe-oa, q27]
---
# Drill: a payment ledger with three-state idempotency and partial refunds

Sixty minutes, no `PART` header — a single ledger accumulates every command.
`PAYMENT id amount ts` records a charge; `REFUND rid payment_id amount ts`
records a refund against it; `REVENUE` (optionally with `start_ts end_ts`)
reports net cents; `PAYMENTS date` lists payment ids on a calendar day;
`TRANSACTIONS` lists every recorded movement as a Stripe-style balance-
transaction row with a running net. Both `PAYMENT` and `REFUND` ids are
idempotent in three states: a replay with identical fields is a silent
no-op that still returns success; a replay with the same id but different
fields is rejected outright, leaving the original untouched; a genuinely new
id is recorded. A refund additionally requires the payment to exist, the
cumulative refunded amount to never exceed the payment amount, and the
refund's timestamp to be at or after its payment's timestamp.

**Constraints to state and honor**
- Timestamps are the exact form `YYYY-MM-DDTHH:MM:SS`; anything else (a
  missing `T`, a nonexistent calendar date, an out-of-range hour) is a bad
  timestamp — a business rejection (`REJECTED`) on `PAYMENT`/`REFUND`, a
  parse error (`ERROR`) in a `REVENUE` query.
- Amounts are positive integer cents; `amount <= 0` is always rejected.
- `REVENUE start end` is inclusive on both ends and counts each event by its
  *own* timestamp — a refund inside the range with its payment outside can
  make the range total negative.
- Rejected or replayed requests never appear in `TRANSACTIONS` and never
  change any accumulated total.

**Grading points**
- The idempotency check runs before any business validation, and is
  explicitly three states, not two — same id/same fields (no-op success),
  same id/different fields (reject, keep original), new id (record) — stated
  as a named rule rather than left implicit in the code.
- The refund cap is `<=`, so refunding exactly the remainder succeeds and one
  more cent fails; a rejected refund must not partially consume the cap.
- A refund timestamp equal to its payment's timestamp is accepted; one second
  earlier is rejected — say why fixed-width timestamp strings make this a
  plain string (or lexicographic) comparison rather than requiring full
  datetime parsing.
- `get_payments_by_date` sorts by timestamp then id and excludes refunds
  entirely; `get_balance_transactions` orders by timestamp, then payments
  before refunds at an identical timestamp, then id, accumulating a running
  net across the whole sorted sequence in one pass.
- Range revenue with an open end (`None`) versus a fully bounded range are
  both exercised, along with a range that produces a negative total.
- Four distinct bad-timestamp shapes are worth naming: missing `T`, wrong
  separator, an invalid calendar date, and an out-of-range hour like `24:00`.

**Source**
- `vault/Quick_Check/problems/q27_payment_ledger/problem.md`, `vault/Quick_Check/problems/q27_payment_ledger/REPORT.md`, `vault/Quick_Check/study/10-solutions/q27_payment_ledger.md`.

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):

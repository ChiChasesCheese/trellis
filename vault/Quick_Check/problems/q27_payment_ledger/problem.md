# q27 · PaymentLedger — idempotent payments, partial refunds, revenue by range, balance transactions

**Type:** bespoke intern VO coding · **Stage:** virtual onsite coding round (45–60 min) · **Last asked:** 2026-04-13 (programhelp intern VO)
**Frequency:** 4 independent reports (programhelp 2026-01-26, 2026-03-31, 2026-04-02, 2026-04-13 intern VO write-ups; en_forums.md §20) · **Confidence:** medium — the four method names, payment-id idempotency, partial refunds and time-range revenue are consistent across reports; exact return values, the balance-transaction rows and the command stream are **reconstructed** (marked).

## Context
Every Stripe charge and refund lands in a ledger. Clients retry requests, so the ledger must be
**idempotent** on the caller-supplied id (Stripe's idempotency keys: replaying an identical request
is a no-op, replaying with different parameters is an error). Refunds may be partial and repeated
until the payment is fully refunded, never beyond, and never before the payment happened.
Finance asks for net revenue over a date range and for the Stripe-style **balance transaction**
list (one signed row per movement with the running net).

## Input (stdin) — one command per line, rules accumulate (no `PART` header)
```
PAYMENT <payment_id> <amount_cents> <ts>                    -> OK | REJECTED
REFUND  <refund_id> <payment_id> <amount_cents> <ts>        -> OK | REJECTED
REVENUE                                                     -> net cents over everything
REVENUE <start_ts> <end_ts>                                 -> net cents with ts in [start, end]
PAYMENTS <YYYY-MM-DD>                                       -> id1,id2,... | NONE
TRANSACTIONS                                                -> one line per row, or NONE
```
`ts` is `YYYY-MM-DDTHH:MM:SS` (no timezone, no fractions — anything else is a bad timestamp).
Amounts are integer minor units (cents). Blank lines are ignored. An unknown verb, wrong arity,
non-integer amount, or a bad timestamp in `REVENUE` prints `ERROR` (Part 4); a bad timestamp
in `PAYMENT`/`REFUND` is a business rejection and prints `REJECTED`.

## Class API
```
PaymentLedger()
  add_payment(payment_id, amount_cents, ts) -> bool
  add_refund(refund_id, payment_id, amount_cents, ts) -> bool
  get_total_revenue(start_ts=None, end_ts=None) -> int
  get_payments_by_date(date) -> list[str]
  get_balance_transactions() -> list[tuple[str, str, int, int]]      # (type, id, amount, net)
```

## Rules
### Part 1 — payments and total revenue
`add_payment` accepts `amount_cents > 0` and a well-formed `ts`, returns `True`.
**Idempotency on `payment_id`** (reconstructed from "payment_id 幂等"): the same id with the
**same amount** is a silent no-op (`True`, nothing recorded twice — the timestamp of the replay is
ignored); the same id with a **different amount** is rejected (`False`), the original stays.
`amount_cents <= 0` → rejected. `get_total_revenue()` = sum of payments − sum of refunds.

### Part 2 — partial refunds
`add_refund` requires: known `payment_id`; `amount_cents > 0`; **cumulative** refunds of that
payment ≤ payment amount (`<=`: refunding the exact remainder is fine, one cent more is not);
`refund ts >= payment ts` (a refund before its payment is rejected); well-formed `ts`.
Idempotent on `refund_id`: same id with the same `(payment_id, amount)` → no-op `True`; same id
with anything different → `False`. Rejected refunds never change the cumulative total.

### Part 3 — time-range revenue and payments by date
`get_total_revenue(start_ts, end_ts)` counts every payment and every refund whose **own** `ts`
lies in `[start_ts, end_ts]` (both inclusive; `None` = open end). A refund inside the range counts
even if its payment is outside, so a range total can be negative. `get_payments_by_date(date)`
returns the ids of payments whose `ts` falls on that calendar day, sorted by `ts` then by id
(plain string order); refunds are not payments. Bad timestamps in queries are errors.

### Part 4 — balance transactions (reconstructed, Stripe `balance_transaction` style)
`get_balance_transactions()` returns one row per recorded movement, `(type, id, amount, net)`:
`type ∈ {payment, refund}`, `amount` signed cents (refunds negative), `net` = running total after
this row. Rows are ordered by `ts`, then payments before refunds at the same `ts`, then id.
Replays and rejected requests produce no rows. The command prints `type,id,amount,net` per row.

## Worked examples
**Example 1 — everything**
```
PAYMENT p1 1000 2026-03-01T10:00:00                OK
PAYMENT p2 2500 2026-03-01T12:30:00                OK
PAYMENT p1 1000 2026-03-02T00:00:00                OK          (replay: no-op)
PAYMENT p1 999 2026-03-01T10:00:00                 REJECTED    (same id, different amount)
PAYMENT p3 0 2026-03-01T13:00:00                   REJECTED    (amount must be > 0)
PAYMENT p4 500 2026-03-01                          REJECTED    (bad timestamp)
REVENUE                                            3500
REFUND r1 p1 400 2026-03-01T11:00:00               OK
REFUND r1 p1 400 2026-03-05T00:00:00               OK          (replay)
REFUND r2 p1 600 2026-03-02T09:00:00               OK          (cumulative 1000 == payment)
REFUND r3 p1 1 2026-03-02T09:30:00                 REJECTED    (over-refund)
REFUND r4 p2 100 2026-03-01T12:00:00               REJECTED    (before the payment)
REFUND r5 px 100 2026-03-01T12:00:00               REJECTED    (unknown payment)
REVENUE                                            2500
REVENUE 2026-03-01T00:00:00 2026-03-01T23:59:59    3100        (1000 + 2500 − 400)
REVENUE 2026-03-02T09:00:00 2026-03-02T09:00:00    -600        (inclusive both ends: r2 only)
PAYMENTS 2026-03-01                                p1,p2
PAYMENTS 2026-03-02                                NONE
TRANSACTIONS
payment,p1,1000,1000
refund,r1,-400,600
payment,p2,2500,3100
refund,r2,-600,2500
```
**Example 2 — ordering**
```
PAYMENT b 100 2026-01-01T00:00:00     OK
PAYMENT a 100 2026-01-01T00:00:00     OK
PAYMENT c 100 2025-12-31T23:59:59     OK
REFUND  z a 100 2026-01-01T00:00:00   OK        (same second as the payment: allowed)
PAYMENTS 2026-01-01                   a,b       (same ts -> id order)
PAYMENTS 2025-12-31                   c
TRANSACTIONS
payment,c,100,100
payment,a,100,200
payment,b,100,300
refund,z,-100,200
```
**Example 3 — empty ledger and errors**
```
REVENUE                               0
PAYMENTS 2026-01-01                   NONE
TRANSACTIONS                          NONE
REVENUE 2026-01-01 2026-01-02         ERROR
PAYMENT p1 12.5 2026-01-01T00:00:00   ERROR
FOO                                   ERROR
```

## Edge cases hidden tests are known to target
- replay with same amount → OK and counted once; replay with different amount → REJECTED and the original stands
- refund exactly the remaining amount (==) accepted; one cent more rejected; several partial refunds summing to the total
- refund at the same second as the payment accepted; one second earlier rejected
- refund replay with same fields OK, with a different amount/payment REJECTED; rejected refunds don't consume the cap
- unknown payment id; `amount <= 0` for both payments and refunds
- bad timestamps: `2026-03-01`, `2026-03-01 10:00:00`, `2026-02-30T00:00:00`, `2026-03-01T24:00:00`
- range revenue inclusive at both ends; refund inside the range with its payment outside → negative
- `get_payments_by_date` sorted by ts then id, ignores refunds, `NONE` when empty
- balance rows: payment before refund at equal ts, running net, no rows for replays/rejections
- large values (10^9 cents × 10^5 rows) — integers only

## Variants seen in the wild
- `add_refund(refund_id, amount, ts)` without an explicit `payment_id` (refund keyed to the
  payment by the id it names) — programhelp 2026-03-31 wording; the H6 report says "4 methods".
- Follow-ups in the same round: "what if two threads add the same payment" (idempotency key +
  lock), "float precision" debugging on `amount` (use cents), "what does Stripe return on an
  idempotent replay" (the original response).
- Some reports add `get_refunds_for_payment(payment_id)`; trivial from the per-payment list.

## What this tests
skills: S03 class + dict modeling · S06 integer money · S11 idempotency/de-duplication ·
S12 timestamp parsing and inclusive ranges · S08 deterministic ordering · S17 ledger-style
tracking · S18 validation/error paths · S19 incremental design

## Sources
- https://programhelp.net/en/vo/stripe-vo-interview-questions-and-solutions/ (H1, 2026-04-02 VO: PaymentLedger, idempotent add_payment/refund/get_payments_by_date)
- https://programhelp.net/en/vo/stripe-intern-vo-coding-debug-integration-guide/ (H2, 2026-03-31 intern VO: PaymentLedger; float-precision debug)
- https://programhelp.net/en/vo/stripe-summer-intern-vo-coding-integration/ (H4, 2026-01-26 intern VO)
- https://programhelp.net/en/vo/stripe-intern-vo-coding-integration/ (H6, 2026-04-13 intern VO: PaymentLedger 4 methods)
- catalog/raw/en_forums.md §20 (follow-ups: partial refunds, time-range queries, bad timestamps); cn_sources.md §3 "PaymentLedger 类"

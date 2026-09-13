# q27 PaymentLedger — report

## Summary
Intern virtual-onsite coding round (four independent 2026 reports): a small ledger class with
idempotent `add_payment`, partial `add_refund` under a cumulative cap and a timestamp ordering rule,
net revenue over an inclusive timestamp range, payments by calendar day, and (reconstructed
Part 4) Stripe-style balance-transaction rows with a running net. It is Stripe's idempotency-key
and refund semantics reduced to a class the interviewer can grill edge cases on.

## Sources & confidence
medium — programhelp intern VO write-ups 2026-01-26 (H4), 2026-03-31 (H2), 2026-04-02 (H1),
2026-04-13 (H6); en_forums.md §20 lists the follow-ups (partial refunds, time-range queries, bad
timestamps). Return values, replay semantics (same amount → no-op, different amount → reject),
`net` = running total, and the command stream are reconstructed and marked in problem.md.

## Approach by part
1. `payments: dict[id, Payment(amount, ts, refunded)]`; replay check happens *before* validation
   (a retried request with the same amount is a no-op even with a different/bad ts); amount > 0;
   ts validated by `strptime` + round-trip `strftime` so only the exact zero-padded form passes.
2. Refund: known payment, amount > 0, valid ts, `ts >= payment.ts` (string compare works because
   the format is fixed-width), `refunded + amount <= payment.amount` (== allowed); refund ids are
   idempotent on `(payment_id, amount)`; rejected refunds never touch `refunded`.
3. Events are bucketed by day with a per-day total: a range query adds whole-day totals for days
   strictly inside the range and filters only the two edge days with inclusive bounds; `None`
   means open-ended; bad timestamps raise `ValueError` (→ `ERROR` in the stream).
   `get_payments_by_date` sorts that day's payment events by `(ts, id)`.
4. `get_balance_transactions` sorts all events by `(ts, kind, id)` with payment < refund and
   accumulates the running net; refunds carry negative amounts.

## Pitfalls hidden tests target
replay same-amount OK / different-amount REJECTED with the original intact; cap boundary
(exact remainder OK, +1 cent rejected) and rejected refunds not consuming the cap; refund at the
same second OK, one second earlier rejected; strict timestamp format (`2026-3-1…`, `…Z`,
`2026-02-30`, `T24:00:00` all bad); inclusive range on both ends and negative range totals;
sort by ts then id, refunds excluded from payments-by-date; same-ts ordering of balance rows;
10^9-cent amounts (integers only).

## Complexity & measured cost
`add_*` O(1); range revenue O(#days + edge-day events); payments-by-date O(k log k);
balance transactions O(n log n). 100k events + 200 range queries + 200 by-date queries + one
full TRANSACTIONS dump (100k rows): 0.69 s, 103 MB.
Measured: 0.694s, 102.8 MB

## Test inventory
17 tests — part1: 3 · part2: 4 · part3: 5 · part4: 5; edge 7 · fmt 2 · io 1 · perf 1.
`IMPL=starter`: 17 failed / 0 passed.

## Skills exercised
S03 class + dict modeling · S06 integer money · S08 deterministic ordering · S11 idempotency ·
S12 timestamp parsing + inclusive ranges · S17 ledger tracking · S18 validation/error paths ·
S19 incremental design

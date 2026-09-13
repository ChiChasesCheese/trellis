---
nodes: [rules.rounding, rules.fees, rules.grouping, transfer.stripe-oa]
tags: [stripe-oa, q20]
---
# Drill: fee schedule, rate-table override, payout rollup and ledger reconciliation

Sixty minutes, four parts, CSV rows read by header (column order and extra columns don't
matter). Part 1 computes a per-transaction processing fee from its status: a percentage
plus a fixed amount on a completed payment, a flat fee on a lost dispute, a
provider-dependent fee on a won dispute, zero otherwise. Part 2 overrides the default with
a `(provider, country)` rate table that has its own, different rounding rule and a
four-level wildcard precedence. Part 3 groups transactions into payout-level receivables by
merchant, card type and payout date. Part 4 reconciles a system ledger against a gateway
ledger and reports what's missing or mismatched.

**Constraints to state and honor**
- Amounts are integer cents (a decimal like `10.00` converts exactly); up to 10^5 CSV rows,
  up to 2×10^5 for the reconciliation part.
- Part 1's percentage rounds half-up to the cent; Part 2's rate-table fee floors instead —
  the same problem uses two different rounding rules on purpose.
- Part 2's rate table never applies to dispute rows, only to completed payments.
- Part 4 sums duplicate transaction ids on the same side before comparing.

**Grading points**
- The half-up percentage done in integers — `(amount*21 + 500)//1000 + 30` — not a float
  multiply, and a candidate should be able to hand-check `500 -> 41` (banker's rounding
  would wrongly give 40).
- Wildcard precedence for the rate table is a strict four-step fallback — exact pair,
  provider-only, country-only, both-wildcard, then the Part 1 default — checked in that
  order, not "closest match wins" by some other metric.
- Receivables grouping computes `net = amount - fee` per row and sums by group; fee is 0
  when the row has no `status` column at all (a genuinely different input shape from the
  same problem family), not an error.
- Groups whose net is zero or negative are still printed; the header line prints even when
  there are no data rows.
- Reconciliation output is one line per transaction id in sorted order —
  `MISSING_IN_GATEWAY`, `MISSING_IN_SYSTEM`, or `AMOUNT_MISMATCH id sys gw` — with nothing
  printed for a match unless matches are explicitly requested.
- `csv.DictReader` (or equivalent) used from the start, so column reordering and extra
  columns are a non-issue rather than a parsing special case.

**Source**
- The full statement, solution notes and report: `vault/stripe/q20_transaction_fees_reconciliation/question.md`,
  `vault/stripe/q20_transaction_fees_reconciliation/solution.md`,
  `vault/Quick_Check/problems/q20_transaction_fees_reconciliation/problem.md`.

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):

---
nodes: [rules.grouping, rules.thresholds, transfer.stripe-oa]
tags: [stripe-oa, q02]
---
# Drill: score merchants over three independent rule passes

Sixty minutes, stdin to stdout, no libraries beyond the standard one. Each
merchant starts at a base score, and every transaction in the input is paired
1:1 (by position) with a rule. Apply three scoring rules as three *separate*
full passes over the transaction list — not interleaved per transaction: an
amount-threshold multiplier, a repeat-customer bonus, and an hourly-density
bonus/penalty that depends on the time of day. Print the final score for
every merchant, including merchants with zero transactions.

- Part 1: parse the three sections and apply only the amount-multiplier pass.
- Part 2: add the repeat-customer pass, counted per `(merchant, customer)`.
- Part 3: add the hourly-density pass, counted per `(merchant, customer, hour)`,
  with the sign of the adjustment depending on the hour band.

**Constraints to state and honor**
- Input arrives as three labeled sections (merchants, transactions, rules);
  the i-th rule belongs to the i-th transaction, same order.
- Up to ~1000 merchants and 1000 transactions; all values are integers (amount
  in minor units).
- The amount check is strictly `>`, not `>=`; zero/negative amounts never
  trigger it.
- Output one line per merchant sorted by id in plain string order, format
  `merchant_id, score` (comma + one space); scores may be negative, printed as-is.

**Grading points**
- Three passes as three separate functions/loops over the full transaction
  list, gated by which part is requested — not one loop that tries to do
  everything, and not the multiplier applied after additive terms have
  already landed (the multiplier only ever scales the original base score).
- Strict `>` on the amount threshold, called out explicitly, since `>=` is the
  single most common failure mode reported for this problem.
- Two independent running counters — `(merchant, customer)` for the repeat
  bonus and `(merchant, customer, hour)` for the density rule — that both
  include the *current* transaction when deciding whether the running count
  has reached 3, so the 2nd transaction of a pair never fires and the 3rd
  always does.
- Using the *current* transaction's rule fields when adding, not the first
  transaction's of that group; duplicate identical transaction lines are
  independent transactions and increment both counters separately.
- Hour-band sign logic exercised at every boundary: 12-17 adds, 9-11 and
  18-21 subtract, everything else (0-8, 22-23) does nothing.
- Merchants with no transactions still print at their base score; output
  sorted by plain string order (`m10` before `m2`), exact `, ` separator.

**Source**
- `vault/interviews/companies/stripe/problems/q02_merchant_fraud_score/problem.md`
- `vault/interviews/companies/stripe/study/10-solutions/q02_merchant_fraud_score.md`
- `vault/interviews/companies/stripe/problems/q02_merchant_fraud_score/problem.md`
- `vault/interviews/companies/stripe/problems/q02_merchant_fraud_score/REPORT.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):

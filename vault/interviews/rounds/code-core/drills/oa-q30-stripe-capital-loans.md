---
nodes: [rules.rounding, input.malformed, transfer.stripe-oa]
tags: [stripe-oa, q30]
---
# Drill: Stripe Capital loan ledger — pay, increase, withhold, reject

Sixty minutes, stdin to stdout, one command per line with no PART header — every rule accumulates
into a single program instead of unlocking in stages. Each line is `METHOD: params` against a
per-merchant, per-loan ledger in integer cents: CREATE_LOAN opens a loan, PAY_LOAN repays it
manually, INCREASE_LOAN adds to it, and TRANSACTION_PROCESSED withholds a percentage of a sale
amount and applies it as a payment toward a named loan. After all lines, print every merchant with
positive total outstanding debt — loan balances summed across all of that merchant's loans —
sorted by merchant id, skipping merchants who owe nothing. Any line naming an unknown merchant or
loan, carrying a negative amount, an out-of-range percentage, a duplicate loan creation, or an
unrecognized method is a silent no-op.

**Constraints to state and honor**
- Loan ids are scoped per merchant — `loan1` under two different merchants are independent
  balances that must never collide.
- A repayment, manual or via transaction, never drives a loan below 0; the excess is discarded,
  not carried over to another loan of the same merchant.
- The withheld amount from a transaction is `amount * pct // 100`, truncated toward zero, never
  rounded to the nearest cent.
- Balances reach up to 10^12 cents across up to 10^5 lines — integers only, no floating point
  anywhere in the pipeline.
- Output format is `merchant_id,total` with no space and no currency symbol; merchants at an
  all-zero balance are omitted entirely, including ones just created with amount 0.

**Grading points**
- One validation gate in front of every mutation — unknown merchant, unknown loan, negative
  amount, out-of-range percentage, duplicate create — rather than five scattered checks; say out
  loud it's the same guard reused across all four methods.
- `balance = max(0, balance - amount)` as the single primitive both PAY_LOAN and
  TRANSACTION_PROCESSED reduce to.
- Truncating division tested at the boundary that actually zeroes out (`99 * 1 // 100 == 0`), not
  just an example that happens to round cleanly.
- A duplicate `CREATE_LOAN` on an existing (merchant, loan) pair is ignored, keeping the original
  balance — state this choice explicitly, since the sources disagree (some implementations
  replace or add instead of ignoring).
- Lexicographic sort on merchant id, checked against `m10` vs `m2` and `acct_barfoo` vs
  `acct_foobar`, not a numeric or insertion-order sort.
- Trimming stray spaces after commas in parameters (`merchant1, loan1, 1000`) as part of parsing,
  not as a per-method special case.

**Source**
- `vault/interviews/companies/stripe/problems/q30_stripe_capital_loans/problem.md`, `vault/interviews/companies/stripe/problems/q30_stripe_capital_loans/REPORT.md`, `vault/interviews/companies/stripe/problems/q30_stripe_capital_loans/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q30_stripe_capital_loans.md`, `vault/interviews/companies/stripe/study/10-solutions/q30_stripe_capital_loans.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):

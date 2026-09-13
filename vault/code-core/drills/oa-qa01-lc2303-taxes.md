---
nodes: [rules.tiers, rules.rounding]
tags: [stripe-oa, qa01, leetcode]
---
# Drill: graduated tax brackets, per-band breakdown, integer cents and volume pricing

Forty-five minutes, stdin to stdout. This is LeetCode 2303, Calculate Amount
Paid in Taxes, grown into Stripe's own graduated-versus-volume tiering: given
brackets of strictly increasing upper bounds and percentages, and an income,
compute the total tax. Part 1 is the LeetCode signature itself, walking the
brackets and summing each band's taxed slice. Part 2 returns the
per-bracket breakdown line by line, the kind of detail an invoice would
show, keeping only bands with a nonzero taxable slice. Part 3 redoes the
computation in integer cents with each band's tax rounded half-up
independently before the lines are summed, never floating point. Part 4 adds
a volume mode where the whole income is taxed at the rate of whichever
single bracket contains it, instead of band by band.

**Constraints to state and honor**
- Brackets are given as `upper,percent` lines with strictly increasing
  uppers, guaranteed to cover the given income.
- Part 1 accepts and must return a value accurate to a small float
  tolerance; Parts 3–4 stay in exact cents or a fixed two-decimal format.
- A band's taxable slice is `min(income, upper_i) - upper_{i-1}`, clamped to
  zero; income sitting exactly on an upper bound belongs to that bracket,
  not the next.
- Part 3 rounds each band's tax half-up to the cent independently, before
  summing — not the total once.
- Part 4's volume mode taxes the whole income at the rate of the first
  bracket whose upper is ≥ income.

**Grading points**
- Compute each band's tax as an integer numerator over 100 rather than
  accumulating floats across many brackets — say why (drift over 100
  brackets) rather than discovering it in a failing test.
- Part 2's breakdown must reproduce Part 1's total exactly when summed —
  treat that as an invariant to assert, not just a nice property.
- Half-up rounding is a deliberate choice over banker's rounding, and it
  must be applied per band: state that rounding the total once gives a
  different (also defensible, but different) answer, and pick one.
- The boundary rule — income exactly on an upper bound stays in that
  bracket — has to hold in both graduated and volume mode.
- Zero income and a zero-percent bracket are real test cases: a 0% bracket
  still produces a breakdown line, but zero income produces none.

**Source**
- `vault/stripe/qA01_lc2303_taxes/question.md`, `vault/stripe/qA01_lc2303_taxes/solution.md`, `vault/Quick_Check/problems/qA01_lc2303_taxes/problem.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):

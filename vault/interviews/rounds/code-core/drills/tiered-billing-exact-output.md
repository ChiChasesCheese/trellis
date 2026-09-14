---
nodes: [rules.tiers, rules.money, rules.rounding, rules.grouping, output.formatting, output.ordering, verification.tests]
tags: [classic]
---
# Drill: tiered billing with an exact-output contract

Forty minutes. One line per usage record: `account_id,units_a,units_b,plan`.
Two plans exist — metered, billed per complete block of 100 units at different
rates for the two unit kinds, and subscription, a flat monthly fee that includes
an allowance of combined units, with overage billed at the metered rates. An
account may appear on both plans in the same period, in which case the fee and
the allowance are prorated by the *share of records* on the subscription plan,
with the fee rounded half-up to the cent and the allowance floored.

Print one line per account, `account_id: $x.xx`, sorted by account id in plain
string order. Every account appears, including those owing $0.00.

**Constraints to state and honor**
- Up to 10^5 records; unit counts up to 10^9; 2 s, 256 MB.
- Integer minor units end to end — no float touches money.
- Blocks are floored per record; remainders never pool across records.

**Grading points**
- Half-up rounding done in integers, once, at the edge — `(2*fee*k + n) // (2*n)`
  rather than a float multiply ([[cc-python-stdlib-decimal-calls]]).
- The allowance is consumed in record order, first unit kind before the second,
  and the boundary case where it runs out mid-record.
- Exactly-at-allowance produces zero overage; one unit more produces one block
  ([[cc-verification-edge-exact-threshold-triple]]).
- $0.00 accounts still printed ([[cc-verification-edge-empty-and-single]]).
- Formatting in one function, at write time ([[cc-python-io-exact-stdout]]).
- Two or three tests per part, one of them re-running part 1's example
  ([[cc-verification-tests-two-or-three-per-part]]).

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):

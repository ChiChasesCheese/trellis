---
nodes: [algorithms.settlement, algorithms.backtracking, rules.money, output.ordering, performance.budget]
tags: [classic]
---
# Drill: settling a group of debts in the fewest transfers

Thirty-five minutes. Lines of `from,to,amount_minor` record who owes whom. Net
every participant down to a single balance, then output the minimum number of
transfers that settles everyone to zero, followed by the transfers themselves in
a deterministic order.

**Constraints to state and honor**
- At most 12 participants with a non-zero net balance; amounts are integers in
  minor units.
- Participants who net to zero must not appear in any transfer.
- Total of all balances is zero — assert it before starting.
- Output the count first, then `from,to,amount` lines sorted by `(from, to)`.

**Grading points**
- Netting first is what makes the search small: the input size is the number of
  edges, the search size is the number of non-zero balances.
- Recognize that minimum-transfers is exponential in the number of participants,
  and that the stated bound of 12 is the statement telling you so
  ([[cc-performance-budget-small-n-unlocks]]).
- Backtracking with a canonical order and pruning that cannot discard an optimum;
  or bitmask DP over subsets that each sum to zero.
- The conservation invariant — balances sum to zero before and after every
  transfer ([[cc-verification-invariant-conservation]]).
- Integer minor units throughout; a settlement that leaves one unit unassigned is
  a rounding bug, not a tie ([[cc-python-pitfalls-float-equality]]).
- Deterministic output when several optimal settlements exist
  ([[cc-verification-determinism-set-iteration]]).

**Attempt log**
- [ ] Attempt 1 (date, 35 min, self-graded notes):

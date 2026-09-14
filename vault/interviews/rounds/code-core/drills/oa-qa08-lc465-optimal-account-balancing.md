---
nodes: [algorithms.settlement, algorithms.backtracking]
tags: [stripe-oa, qa08, leetcode]
---
# Drill: net a pile of IOUs down to the fewest possible transfers

Forty-five minutes, stdin to stdout. This is LeetCode 465, Optimal Account
Balancing. You're given `[from, to, amount]` records meaning `from` handed
`amount` to `to` — so `to` owes `from` that much back. Part 1 asks for the
minimum number of transfers that leaves every party's net balance at zero,
where any party may pay any other; the transfers need not follow the
original edges. Part 2 asks for one such optimal transfer list, produced
deterministically. Part 3 adds a dust write-off: since every transfer costs
a flat fee, any party whose net balance's absolute value falls strictly
below a given threshold has their claim forfeited or debt forgiven instead
of settled, with a virtual `PLATFORM` party absorbing whatever residual that
leaves behind, before running Part 2's search on what remains.

**Constraints to state and honor**
- Up to 8 transactions over up to 12 parties, so after netting there are at
  most 12 parties with a non-zero balance — small enough for exact search,
  not for a claimed polynomial algorithm (the general problem is NP-hard).
- Net every party first (`given - received`) and drop parties that net to
  zero before searching; the remaining nets always sum to zero.
- The answer is `n - (max number of disjoint zero-sum subsets)`, not the
  naive "everyone pays one hub" guess of `n - 1`.
- Part 2's output must be deterministic: process parties and candidate
  partners in ascending id order, and keep the first transfer list that
  achieves the minimum count.
- Part 3: `0 < |net| < threshold` is written off (strict — a net exactly
  equal to the threshold is still settled); if the remaining nets don't sum
  to zero on their own, add a `PLATFORM` party for the residual.

**Grading points**
- Net first, drop zeros, then search only over the non-zero nets — say out
  loud why a pass-through party with net zero must never enter the search.
- The DFS should settle one party completely per transfer against an
  opposite-sign partner, and justify why that loses no generality (some
  optimal solution settles at least one party per transfer).
- Real pruning, not hand-waving: skip a candidate whose current value
  repeats one already tried at this level, stop the loop right after an
  exact cancellation (never worse than continuing), and cut a branch that
  can no longer beat the best count found.
- Cross-check the DFS against a bitmask DP over the non-zero nets
  (`dp[mask] = max_i dp[mask without i] + [sum(mask) == 0]`, answer
  `n - dp[full]`) — both must agree on every input.
- Determinism in Part 2 comes from search order, not from sorting the
  output after the fact; a chain where a party is over-paid and forwards
  the excess later is a legitimate optimal answer, not a bug.
- Part 3's write-off must never emit a `PLATFORM` transfer when the
  written-off nets happen to cancel exactly.
- Edge cases: sign convention getting flipped reverses every transfer
  direction; one debtor owing k creditors needs exactly k transfers
  regardless of amounts; duplicate nets must change only speed, never the
  answer.

**Source**
- `vault/stripe/qA08_lc465_optimal_account_balancing/question.md`, `vault/stripe/qA08_lc465_optimal_account_balancing/solution.md`
- `vault/Quick_Check/problems/qA08_lc465_optimal_account_balancing/problem.md`, `vault/Quick_Check/problems/qA08_lc465_optimal_account_balancing/REPORT.md`
- `vault/Quick_Check/study/10-solutions/qA08_lc465_optimal_account_balancing.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):

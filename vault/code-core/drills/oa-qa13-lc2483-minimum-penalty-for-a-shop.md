---
nodes: [algorithms.prefix, algorithms.dp]
tags: [stripe-oa, qa13, leetcode]
---
# Drill: pick a closing hour with a running penalty, then choose the whole schedule

Forty-five minutes, stdin to stdout. This is LeetCode 2483, Minimum
Penalty for a Shop, taken past the LC signature into scheduling territory
the bespoke store-closing problem doesn't cover. `customers` is a string of
`Y`/`N` per hour. Part 1 finds the closing hour `j` (open during `0..j-1`,
closed after) minimizing penalty — idle open hours plus missed customers —
returning the earliest `j` on ties. Part 2 lets the shop choose both an
opening and a closing hour, i.e. one contiguous open window, minimizing the
same penalty. Part 3 allows up to `k` disjoint open windows (split shifts).
Part 4 returns to a single close-only decision but with a non-negative
weight per hour, so the penalty of an idle or missed hour scales by that
hour's cost.

**Constraints to state and honor**
- `1 <= n <= 10^5`; the whole drill must be solvable in O(n) or O(n*k), an
  O(n^2) per-hour recount will time out on the hidden tests.
- Closing at hour 0 (never open) and at hour n (never close) are both legal
  answers.
- Every part breaks ties toward the earliest hour (or smallest open, then
  smallest close in Part 2) using a strict comparison when updating the
  best-so-far, not `<=`.
- Part 2's window is half-open `[open, close)`, with `open == close` meaning
  the shop never opens; an empty window must be considered.
- Part 3's windows must be disjoint — no double-counting an hour's score
  across two windows; `k = 0` and `k` larger than the number of `Y`-runs are
  both valid inputs.
- Part 4's weights are non-negative and can be zero, which can produce wide
  ties still broken by earliest hour.

**Grading points**
- Part 1 is a single running-penalty pass: start from "closed all day" and
  adjust by +-1 as the boundary moves past each hour, never recomputing the
  full penalty from scratch.
- Recognize Part 2 as maximum subarray in disguise: score `Y` as +1, `N` as
  -1, and penalty equals `count(Y) - (best window score)`, with the empty
  window (score 0) always a candidate.
- Part 3 extends that reduction to a k-window DP over prefixes — state the
  recurrence (`g` tracks the best score with the current window ending
  exactly here; `f[i]` tracks the best using up to the window budget so
  far) rather than reaching for a brute-force partition.
- Part 4 is the same running pass as Part 1 with `weights[j]` replacing the
  unit increment/decrement — recognizing it as a strict generalization
  rather than a new algorithm.
- State explicitly why the tie-break must be a strict less-than: ties are
  common (all-N, all-Y, symmetric weight patterns) and silently using `<=`
  returns the latest hour instead of the earliest.
- Edge cases: all `Y`, all `N`, a single character; `k = 1` in Part 3 must
  reproduce Part 2's penalty exactly; Part 4 with uniform weight 1 must
  reproduce Part 1 exactly.

**Source**
- `vault/stripe/qA13_lc2483_minimum_penalty_for_a_shop/question.md`, `vault/stripe/qA13_lc2483_minimum_penalty_for_a_shop/solution.md`
- `vault/Quick_Check/problems/qA13_lc2483_minimum_penalty_for_a_shop/problem.md`, `vault/Quick_Check/problems/qA13_lc2483_minimum_penalty_for_a_shop/REPORT.md`
- `vault/Quick_Check/study/10-solutions/qA13_lc2483_minimum_penalty_for_a_shop.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):

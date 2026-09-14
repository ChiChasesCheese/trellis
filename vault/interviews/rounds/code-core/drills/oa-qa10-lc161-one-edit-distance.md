---
nodes: [algorithms.strings, algorithms.dp]
tags: [stripe-oa, qa10, leetcode]
---
# Drill: one edit apart, then name the edit, then within k via a banded DP

Forty-five minutes, stdin to stdout. This is LeetCode 161, One Edit
Distance. Part 1 returns whether string `s` can become `t` with exactly one
insert, delete, or replace — identical strings are false, since zero edits
is not one edit. Part 2 also counts an adjacent transposition of two
different characters as one edit (the rule Stripe's corrupted-card-number
check needs: a changed digit, or two adjacent digits swapped). Part 3
returns the specific edit that turns `s` into `t` as `kind index [char]`
(insert, delete, replace, or swap; `none` when they aren't one edit apart).
Part 4 generalizes to "within k edits" — full Levenshtein distance,
without the swap — using a banded DP so it stays fast at string lengths up
to 10^4.

**Constraints to state and honor**
- `0 <= len(s), len(t) <= 10^4`; characters are ASCII letters and digits,
  no spaces, and either string may be empty.
- Part 1 must run in a single left-to-right pass, O(n) time, O(1) extra
  space beyond the tail comparison.
- Part 2's swap only counts when the two transposed characters actually
  differ — swapping two equal characters changes nothing and is not an
  edit.
- Part 3's reported index is always the first index where the strings
  differ, even when the whole shorter string is a prefix of the longer one.
- Part 4: an immediate `abs(len(s) - len(t)) > k` short-circuits to false;
  the DP must be banded to only the cells with `|i - j| <= k`, not the full
  O(n*m) table.

**Grading points**
- Find the first mismatch by scanning, never by assuming the extra
  character sits at either end — then equal-length strings need the tails
  after that index to match, and unequal-length strings (differing by one)
  need the shorter's tail from `i` to match the longer's tail from `i+1`.
- State plainly that identical strings return false in Part 1 — this is the
  single most common wrong answer on this problem.
- Part 3's four edit kinds never collide by construction (swap touches two
  positions, replace one, insert/delete change the length) — the
  implementation should make that non-collision structural, not checked
  after the fact.
- Part 4's banded DP needs O(k) memory per row (not O(n)), a mapping from
  absolute column `j` to a band-relative offset, and an early exit once the
  row's minimum value already exceeds `k`.
- Note explicitly that `within_k_edits(s, t, 1)` should equal
  `s == t or is_one_edit_distance(s, t)`, and use that as a cross-check
  between parts.
- Edge cases: two empty strings (false); one empty and one length-1 (true);
  one empty and one length-2 (false); a mismatch at the very last
  character; an inserted or deleted character at the very front.

**Source**
- `vault/stripe/qA10_lc161_one_edit_distance/question.md`, `vault/stripe/qA10_lc161_one_edit_distance/solution.md`
- `vault/Quick_Check/problems/qA10_lc161_one_edit_distance/problem.md`, `vault/Quick_Check/problems/qA10_lc161_one_edit_distance/REPORT.md`
- `vault/Quick_Check/study/10-solutions/qA10_lc161_one_edit_distance.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):

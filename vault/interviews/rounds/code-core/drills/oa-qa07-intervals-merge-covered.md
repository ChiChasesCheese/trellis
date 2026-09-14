---
nodes: [chrono.intervals]
tags: [stripe-oa, qa07, leetcode]
---
# Drill: merge intervals, drop covered ones, then fill gaps with brand labels

Forty-five minutes, stdin to stdout. This drill combines LeetCode 56, Merge
Intervals, and LeetCode 1288, Remove Covered Intervals, then pushes them
toward Stripe's BIN-range framing. Part 1 is LC 56 as stated: given closed
integer intervals in any order, merge every pair that overlaps or touches at
a single point, and return the disjoint intervals sorted by start, using
real-number endpoint semantics. Part 2 is LC 1288: given distinct intervals,
drop every one covered by another (`[a,b]` covered by `[c,d]` when `c <= a`
and `b <= d`) and report how many survive, plus the survivors themselves.
Part 3 takes labelled intervals inside a full range `[lo, hi]` and fills
every gap by extending the interval that already owns the larger side,
merging only consecutive same-label runs that end up touching. Part 4
redoes Part 1's merge with inclusive integer endpoints, where adjacent
integers (`[1,2]` and `[3,4]`) count as touching even though they don't
share a point.

**Constraints to state and honor**
- Input intervals arrive unsorted; up to 10^4-10^5 intervals with
  coordinates up to 10^5, so the whole drill must stay O(n log n).
- Part 1/4: empty input returns empty output; zero-length intervals and
  exact duplicates are valid input.
- Part 2: intervals are distinct per LC, but duplicates fed in anyway must
  be treated as covering each other so only one survives.
- Part 3: all intervals are inclusive integer ranges inside `[lo, hi]`; a
  nested interval keeps its own bounds — only the interval holding the
  current max end is allowed to grow into a gap.
- Part 4's merge condition differs from Part 1's by exactly one `+1` on the
  adjacency test — say why explicitly.

**Grading points**
- One sort plus one linear sweep with a running interval (or running max
  end) does all four parts — the only things that change are the sort key
  and the merge/cover condition.
- Part 2's sort must break ties by end descending, not ascending — explain
  why `[1,10]` sorted after `[1,4]` would otherwise be misjudged as covered.
- Part 3 needs a notion of "holder of the current max end" with an explicit
  tie-break (larger end wins; tie goes to the smaller start, i.e. the
  covering interval), and a final pass that merges only intervals adjacent
  in the sorted order, not any same-label pair anywhere in the list.
- State the real-vs-integer endpoint distinction out loud: Part 1 merges
  intervals sharing a point (`next.start <= cur.end`), Part 4 also merges
  adjacent integers (`next.start <= cur.end + 1`).
- Edge cases: touching endpoints in Part 1 versus non-adjacent touching in
  Part 4; a chain of nested intervals (`[1,10],[2,9],[3,8]`) collapsing to
  one survivor in Part 2; a same-label interval separated by a different
  label staying split in Part 3; a single interval spanning the whole
  `[lo, hi]` range.

**Source**
- `vault/interviews/companies/stripe/problems/qA07_intervals_merge_covered/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/qA07_intervals_merge_covered.md`
- `vault/interviews/companies/stripe/problems/qA07_intervals_merge_covered/problem.md`, `vault/interviews/companies/stripe/problems/qA07_intervals_merge_covered/REPORT.md`
- `vault/interviews/companies/stripe/study/10-solutions/qA07_intervals_merge_covered.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):

---
nodes: [chrono.windows, chrono.parsing]
tags: [stripe-oa, qa05, leetcode]
---
# Drill: alert on repeated key-card use inside an hour, then generalize and go online

Forty-five minutes, stdin to stdout. This is LeetCode 1604, Alert Using Same
Key-Card Three or More Times in a One Hour Period. Swipes arrive as `name
HH:MM` pairs, one card-holder can appear many times in any order, and a worker
gets flagged when they use their card three or more times inside any
one-hour period, the boundary counted as inside. Part 1 reproduces the LC
signature and returns the flagged names, unique and sorted ascending. Part 2
generalizes the fixed `3` and `60` to parameters `k` and `window`. Part 3
turns the batch audit into an online limiter: `swipe(name, time)` returns
allow or deny in real time, using a `limit` instead of `k`, where denied
swipes do not count toward later windows.

**Constraints to state and honor**
- `HH:MM` is 24-hour, zero-padded, all swipes on the same day — there is no
  midnight wrap, so a later-looking time that is actually earlier (`23:30`
  then `00:10`) is a backwards step, not a forward one.
- Input per name is unsorted and may contain exact duplicate timestamps,
  which count as two separate uses.
- The one-hour window is closed on both ends: exactly 60 minutes apart
  triggers, 61 does not.
- Part 2: `k <= 0` or `window < 0` is a `ValueError`; `k = 1` flags every name
  that appears at all.
- Part 3: swipe times per name must be non-decreasing; a step backwards is a
  `ValueError`; a denied swipe is not counted in any future window for that
  name.

**Grading points**
- Parse `HH:MM` to minutes once, group by name, sort each name's times —
  then the one-hour check collapses to comparing `times[i+k-1] - times[i]`
  against `window`, with no real sliding-window bookkeeping needed for the
  batch parts.
- State out loud why sorting turns an "any interval" condition into a
  fixed-span array scan, and why that's an O(n log n) win over pairwise
  comparison.
- Part 3 needs a different structure than Parts 1-2: a per-name list (or
  deque) of only the *allowed* times, evicting entries older than
  `t - window`, because denied swipes must not occupy a later window.
- Boundary discipline: `<=` not `<` on the window, and `t - window` itself
  counts as inside the window in Part 3.
- Output contract: Parts 1-2 print flagged names deduplicated and sorted as
  plain strings; Part 3 prints one `ALLOW`/`DENY` line per swipe in input
  order.
- Edge cases: a name with fewer than `k` swipes can never alert; unsorted
  input per name; identical timestamps as distinct uses; a backwards time
  step raising rather than silently reordering.

**Source**
- `vault/stripe/qA05_lc1604_keycard_alerts/question.md`, `vault/stripe/qA05_lc1604_keycard_alerts/solution.md`
- `vault/Quick_Check/problems/qA05_lc1604_keycard_alerts/problem.md`, `vault/Quick_Check/problems/qA05_lc1604_keycard_alerts/REPORT.md`
- `vault/Quick_Check/study/10-solutions/qA05_lc1604_keycard_alerts.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):

---
nodes: [chrono.parsing, chrono.arithmetic, chrono.intervals, chrono.windows, algorithms.greedy, output.ordering]
tags: [classic]
---
# Drill: merging maintenance windows across timezone offsets

Forty minutes. Each line declares a recurring window as `region,start,end,offset`
where `start` and `end` are `HH:MM` local times and `offset` is a UTC offset such
as `-07:00` or `+05:30`. Convert every window to UTC minutes, merge all
overlapping and touching windows, and report the merged set — plus the largest
gap during which no region is in a window.

**Constraints to state and honor**
- A window may wrap past midnight after conversion; it then becomes two intervals
  on a 24-hour circular axis.
- Endpoints are half-open: `[start, end)`. Two windows that touch at a point
  merge; two that share no point do not.
- Offsets are not all whole hours.
- Output in ascending start order, `HH:MM-HH:MM` in UTC, one per line, and the
  gap on a final line.

**Grading points**
- Convert to one canonical representation (integer minutes from midnight UTC)
  before doing anything else.
- Day wrap handled by splitting, not by a special case inside the merge
  ([[cc-python-portability-integer-division]] for the modulo on a negative offset).
- The merge is sort-by-start then one linear pass with an explicit invariant
  ([[cc-verification-invariant-name-it]]).
- Half-open endpoints applied consistently in both merge and gap
  ([[cc-verification-edge-exact-threshold-triple]]).
- Degenerate inputs: no windows at all, one window covering the full day, two
  identical windows, a zero-length window
  ([[cc-verification-edge-empty-and-single]]).

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):

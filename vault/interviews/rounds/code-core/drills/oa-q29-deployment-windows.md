---
nodes: [chrono.arithmetic, chrono.intervals, transfer.stripe-oa]
tags: [stripe-oa, q29]
---
# Drill: fold regional business hours into UTC free deployment windows

Sixty minutes, stdin to stdout, no timezone library — offsets are decimal hours applied by hand in
minutes, never `zoneinfo` and never a float hour. Regions report local business hours as a
half-open window plus a fixed UTC offset; a deploy must avoid every region's business hours. Part
1 converts one region's local business-hours window to UTC datetimes for a given local date,
handling fractional offsets and day wrap. Part 2 takes a UTC calendar day, gathers every region's
business intervals that touch it — including spillover from the local dates immediately before
and after — merges them, and prints the complement as free windows. Part 3 scans UTC days forward
from a given "now", skipping blackout dates, clipping the first day's windows to start no earlier
than now, and returns the first K windows of at least L minutes. Part 4 gives regions
weekday-specific hours and lists every window of at least L minutes across a 7-day span, with no
K cap and no "now" clipping.

**Constraints to state and honor**
- Offsets are decimal hours with a sign (`+9`, `-8`, `+5.5`, `+5.75`) — convert to minutes
  immediately and stay in integer minutes for every comparison.
- Local windows are half-open `[start, end)`; `end < start` wraps past local midnight, and
  `end == start` means busy the full 24 hours.
- A window never crosses UTC midnight — a free stretch spanning midnight prints as two windows,
  each checked against L independently; a fully free day prints `00:00..24:00`, a fully busy one
  prints nothing.
- Part 3's scan gives up after 366 days; `K = 0` prints nothing; a blackout day is skipped whole,
  not clipped around.
- Part 4's weekday match is judged on the region's local date, so a negative-offset region's
  Friday shift can land on UTC Saturday.

**Grading points**
- Everything in minutes since midnight with `divmod` for the day-shift, never `datetime` timezone
  arithmetic — say out loud why a float hour is unsafe here.
- Part 2's spillover: a large offset pushes a region's local-date hours into UTC day D-1 or D+1,
  so the day being analyzed must pull business intervals from local dates D-1, D, and D+1, not
  just D.
- Merge before complementing: touching intervals (`..08:00` then `08:00..`) join into one, or a
  spurious zero-length free window leaks through.
- Threshold is `>=` on L, and a "now"-clipped first window can drop below L after clipping — check
  length after the clip, not before.
- One per-day free-window function reused by Parts 3 and 4, rather than two separate scans.
- Boundary cases: "now" exactly at a window's start versus its end (end yields no window at all);
  a blackout on the start day itself; a region that covers all 24 hours.
- `24:00` as the end-of-day sentinel, printed distinct from `00:00` of the following line.

**Source**
- `vault/interviews/companies/stripe/problems/q29_deployment_windows/problem.md`, `vault/interviews/companies/stripe/problems/q29_deployment_windows/REPORT.md`, `vault/interviews/companies/stripe/problems/q29_deployment_windows/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q29_deployment_windows.md`, `vault/interviews/companies/stripe/study/10-solutions/q29_deployment_windows.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):

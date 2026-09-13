# q29 Deployment Windows — report

## Summary
Local business hours in many fixed-offset timezones → UTC busy intervals → complement → first K
free windows of length ≥ L from "now", skipping blackout days → weekly view with weekday-specific
hours. It is the release-engineering cousin of the subscription scheduler: pure interval algebra
plus careful date arithmetic (fractional offsets, day wrap, `24:00`), no zoneinfo.

## Sources & confidence
medium — 1point3acres 2026-08-24 "OA UTC Timezone Mapping and Sliding Window" + OJ titles,
InterviewDB "Deployment — OA" (title), PracHub "Schedule Weekly Deployment Windows" (2026-05-09,
minutes-in-week variant with a full spec). The I/O shape here is reconstructed (marked per part in
problem.md); the PracHub variant's Part 1 is supported verbatim as `variant_week_intervals`.

## Approach by part
1. `Rule(name, offset_min, days, start, end)`; `end <= start` → `end += 1440`; UTC = local − offset;
   render `local_date + start − offset` with `datetime`.
2. For UTC day D, every rule contributes intervals from local dates D−2..D+2 shifted by
   `k·1440 − offset`, clipped to `[0, 1440]`; merge (touching merges); complement.
3. Day-by-day scan from `now.date()` (366-day horizon), skip blackout, clip the first day at
   `now`, keep `e − s >= L`, stop at K. Free windows depend only on the weekday → cached ×7.
4. Same scan with a 7-day horizon, no K, no clipping; rules carry weekday sets (`Mon-Fri`,
   `Sat/Sun`, wrap-around ranges like `Sat-Mon`).

## Pitfalls hidden tests target
`+5.5`/`-3.5` offsets (minutes, `Decimal`, no float); business hours spilling from the previous
or next local day (`+14`, `-8` overnight); touching intervals merging (no zero-length window);
`>=` on L including a "now"-clipped first window; now at window start vs end; blackout on the start
day; K = 0 / K > available / 24 h coverage → nothing; `24:00`; windows split at UTC midnight;
weekday judged in local time (a `-8` Friday shift lands on UTC Saturday).

## Complexity & measured cost
Per day O(R·5 log R); the 366-day scan touches 7 cached weekdays → O(7·R log R + days). 1000 rules
that cover the clock (full 366-day scan): 0.045 s; 5000 weekday rules for a week: ~0.1 s.
Measured: 0.045s, 18.3 MB

## Test inventory
21 tests — part1: 5 · part2: 6 · part3: 7 · part4: 3; edge 10 · fmt 2 · io 2 · perf 1.
`IMPL=starter`: 19 fail / 2 pass (the two pass only because the empty starter returns `[]` for
`part1(["2026-03-02"])`-style empty cases and empty stdin).

## Skills exercised
S02 parsing · S05 `>=` threshold · S08 deterministic order · S09 exact formatting · S12 date/time
arithmetic · S13 interval merge/complement with half-open endpoints · S19 incremental design

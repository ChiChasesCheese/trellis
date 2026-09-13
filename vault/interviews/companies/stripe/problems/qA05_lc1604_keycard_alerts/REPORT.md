# qA05 LC 1604 Key-card alerts — report

## Summary
"≥ 3 uses of one key inside any 60-minute window" over unsorted `HH:MM` swipes: parse, group,
sort, fixed-size window. It is q23's rate limiter seen from the audit side (card-testing / API-abuse
alerting). Tag freq 61–63 (2025-06 and 2026-07 mirrors), absent from the >6-month files, so it is a
recent addition to the Stripe tag.

## Sources & confidence
medium-high — liquidslr All 61.2, snehasishroy all 62.5, github_repos.md §30. No dated write-up;
Parts 2–3 are designed follow-ups aligned with q23.

## Approach by part
1. `to_minutes("HH:MM")`; `defaultdict(list)` per name; sort; `any(ts[i+2] - ts[i] <= 60)`;
   `sorted(alerted)` (names already unique per dict key). O(n log n).
2. Same scan with `k` and `window` parameters; `k ≤ 0` / `window < 0` raise.
3. `KeyCardLimiter`: per-name deque of *allowed* swipe minutes; evict `< t - window`; deny when the
   deque already holds `limit` entries; denied swipes are never appended; per-name monotonic clock.

## Pitfalls hidden tests target
- inclusive 60-minute boundary; identical timestamps count as separate uses
- no midnight wrap (`23:30, 23:50, 00:10` is not an alert); zero-padded hours
- unsorted input; the offending triple need not be adjacent in input order
- Part 3: denied swipes must not count; `t - window` itself is inside the window; per-key
  independence; time going backwards for a key is an error

## Complexity & measured cost
Parts 1–2 O(n log n); Part 3 O(1) amortized per swipe. Measured: 0.20s (10^5 swipes in-process +
script run); script run at LC max (10^5 lines) ≈ 0.10 s, ~59 MB. Budget 2 s / 256 MB.

## Test inventory
15 tests — part1: 8 (incl. 1 io, 1 perf) · part2: 3 · part3: 4; edge 6 · fmt 2.

## Skills exercised
A07 window over sorted timestamps · S02 parsing · S04 grouping · S05 threshold semantics · S12 time parsing · S16 sliding window

# qA04 LC 1169 Invalid Transactions — report

## Summary
Radar's simplest velocity rule: flag a charge over 1000, and flag both charges when the same name
appears in two cities within 60 minutes (inclusive). It is the only Stripe-tagged LeetCode problem in
the 6-month bucket of the 2026-07 tag snapshot (freq 100), so it is the most likely 2026 warm-up.
Follow-ups give the review UI its reasons and make the check online with bounded memory.

## Sources & confidence
high (tag) — snehasishroy six-months.csv (100.0, sole entry) / all.csv (87.5), liquidslr All 89.7 /
>6mo 93.2, github_repos.md §30. No dated write-up names it; Parts 2–3 are designed follow-ups.

## Approach by part
1. Parse to `Tx` NamedTuples; group by name; sort by `(time, index)`; two-pointer window
   `[t-60, t+60]` with a `Counter` of cities — invalid iff `window_size - count[own city] > 0`.
   O(n log n); immune to 20k same-minute transactions. Output in input order.
2. `_city_conflicts` lists actual conflicting pairs per index (output-sensitive scan inside the
   window), reasons = `amount>1000` then `city:<other>` ordered by the other's `(time, index)`.
3. `TransactionStream`: per-name deque of the last 60 minutes, evicted on arrival; returns the
   not-yet-reported in-window conflicts then the arrival; raises on time going backwards.

## Pitfalls hidden tests target
- `amount == 1000` valid; `|dt| == 60` conflicts; symmetric flagging of the earlier transaction
- same city / exact duplicates never conflict with each other, but duplicates are each reported
- out-of-order input; O(n²) pair scans on a dense group
- Part 3: `now-60` still inside the window; a duplicate arrival is a new transaction and can be
  flagged itself even if its twin already was; no double reporting

## Complexity & measured cost
Part 1 O(n log n); Part 2 O(n log n + conflicts); Part 3 O(window) per arrival. Measured: 0.29s
(20 × LC-max batch + one 10^5-record stress + script run); script at LC max ≈ 0.02 s, ~16 MB.

## Test inventory
15 tests — part1: 9 (incl. 1 io, 1 perf) · part2: 3 · part3: 3; edge 7 · fmt 0.

## Skills exercised
A05 hash + sort validation · S02 parsing · S04 grouping · S05 threshold semantics · S12 time windows · S16 sliding window

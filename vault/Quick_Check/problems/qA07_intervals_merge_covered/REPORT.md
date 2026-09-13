# qA07 LC 56 Merge Intervals + LC 1288 Remove Covered Intervals — report

## Summary
The interval pair from the Stripe tag (both freq ~61–63): merge overlapping intervals and drop
intervals covered by another. They are the warm-up for q04 Card Range Obfuscation (brand-labelled
BIN ranges with gap filling) and q29 Deployment Windows; Parts 3–4 bring the LC versions to those
bespoke rules (inclusive integer endpoints, labels, covering interval owns the gap).

## Sources & confidence
high (tag) — liquidslr All (LC 56 61.2, LC 1288 61.2), snehasishroy all (LC 56 62.5), TWINSRIRAM
`merge_intervals`, tryexponent / codinginterview.com mentions, github_repos.md §30; Part 3 rules
copied from q04 (en_forums.md §4). No dated candidate write-up names the LC pair.

## Approach by part
1. Sort by `(start, end)`, sweep with a running interval, merge iff `next.start <= cur.end`.
2. Sort by `(start asc, end desc)`, keep `max_end`; survive iff `end > max_end` (strict, so equal
   intervals collapse to one). `uncovered` returns the survivors; the LC function is its length.
3. q04 rules on mutable rows: smallest start → `lo`; largest end (tie → smaller start) → `hi`;
   sweep with a `holder` of the max end (strictly larger end takes over, ties keep the covering
   row) and extend the holder to `next.start - 1` on a gap; finally merge *consecutive* same-label
   rows that touch (`next.start <= cur.end + 1`). Re-wrapped as `Labeled` NamedTuples.
4. Same sweep as Part 1 with `gap = 1` so adjacent integers merge.

## Pitfalls hidden tests target
- touching endpoints merge in Part 1, adjacent integers only in Part 4; zero-length intervals
- Part 2 sort must be end-descending on equal starts; chains; duplicates; touching is not covering
- Part 3: nested interval must not be extended; tie on max end picks the covering one; same label
  separated by another label stays split (consecutive-only merge, as in q04)
- unsorted input everywhere; empty input → empty output

## Complexity & measured cost
All parts O(n log n). Measured: 0.34s (10 × LC max for LC 56 (10^4) and LC 1288 (10^3), three
sweeps over a 10^5-interval stress, plus the script run); script run at LC 56 max ≈ 0.03 s, ~18 MB.
Budget 2 s / 256 MB.

## Test inventory
16 tests — part1: 6 (incl. 1 io, 1 perf) · part2: 4 · part3: 4 · part4: 2; edge 8 · fmt 0.

## Skills exercised
A09 interval merge/covered · S08 deterministic sort with tie-breaks · S13 inclusive intervals & gap filling · S19 incremental design

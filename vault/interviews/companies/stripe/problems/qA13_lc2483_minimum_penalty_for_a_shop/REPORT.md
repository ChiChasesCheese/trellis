# qA13 LC 2483 Minimum Penalty for a Shop — report

## Summary
#1 on the Stripe tag (freq 100) and the LeetCode form of the store-closing phone screen whose bespoke
parts (given-hour penalty, best hour, `BEGIN … END` logs) live in q08 and are only linked here. Part 1
is the O(n) running-penalty pass with earliest-hour ties; the follow-ups go where q08 does not: choose
open *and* close (max subarray), up to k windows (O(n·k) DP), weighted hours.

## Sources & confidence
tag freq 100.0 / 76.7 (liquidslr 2025-06), 100.0 (shreeratn 2025-05), 100.0 / 87.5 (snehasishroy
2026-07); plus q08's nine bespoke sources (pkafel gist, LC 2585038 / 3950781, Hazeera65, TWINSRIRAM,
premjm-67 `MP.java`, …) → high. Parts 2–4 are designed follow-ups.

## Approach by part
1. `best_closing_time_weighted` with unit weights: `cur = Σ w over 'Y'` (close at 0), then per hour
   `cur += -w` for `'Y'`, `+w` for `'N'`; strict `<` keeps the earliest minimum. `penalty(c, j)` is the
   direct count for checking.
2. `best_open_close`: scores ±1, prefix sums; for each `close` the best `open` is the earliest index of
   the minimum prefix (updated with strict `<`); overall best by `(score desc, open, close)`;
   `penalty = count('Y') − score`; empty window allowed. O(n).
3. `min_penalty_k_windows`: k passes of `g = max(g, f_prev[i−1]) + s[i−1]`, `f[i] = max(f[i−1], g)`;
   answer `count('Y') − f[n]`. O(n·k) time, O(n) memory. Verified against exhaustive search (n ≤ 7).
4. Part 1's loop with per-hour weights (zero weights create ties → earliest hour).

## Pitfalls hidden tests target
- ties → earliest hour (`YNYN` → 1); `>=` instead of `<` returns the latest
- closing at `n` and at `0` are both legal answers (`YYYY` → 4, `NNNNN` → 0)
- O(n²) recount per hour times out at 10^5
- Part 2: empty window for all-`'N'`; ties by smallest open then smallest close (`YNY` → `[0,1)`)
- Part 3: `k = 0` → `count('Y')`; windows disjoint; `k = 1` must equal Part 2
- Part 4: free idle hours (`w = 0`) mean "never close" can win; large weights are plain ints

## Complexity & measured cost
Parts 1, 2, 4 O(n) time, O(1)/O(n) extra; Part 3 O(n·k) time, O(n) memory. Measured: 0.16 s for the
perf test (n = 10^5 through Parts 1–4 with k = 5 in-process + one script run); script run alone
(Part 3, k = 5) 0.09 s, ~18 MB. Budget 2 s / 256 MB.

## Test inventory
15 tests — part1: 7 (incl. 1 io, 1 perf) · part2: 3 · part3: 3 · part4: 2; edge 5.

## Skills exercised
A01 prefix sums + argmin with tie-break · S05 tie semantics · S13 boundary discipline · S19 incremental design · S22 time-boxing

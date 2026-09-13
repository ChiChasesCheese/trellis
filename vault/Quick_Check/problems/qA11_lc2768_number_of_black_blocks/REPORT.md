# qA11 LC 2768 Number of Black Blocks — report

## Summary
Sparse-grid counting: 10^4 black cells on a 10^5 × 10^5 grid, how many 2×2 windows hold 0..4 of them.
Iterate the cells, hash the ≤ 4 windows each one touches, get bucket 0 by subtraction. Follow-ups:
k×k windows and streaming paints with an O(1)-maintained histogram — the "update the aggregate,
never recompute" habit of Stripe dashboards/alerting.

## Sources & confidence
tag freq 61.2 / 67.1 (liquidslr 2025-06 All / >6mo), 62.5 / 62.5 (snehasishroy 2026-07); not in
shreeratn 2025-05 → high on tag data, medium (no dated write-up). Parts 2–3 are designed follow-ups.

## Approach by part
1. `_touched(m, n, coords, k)`: dedupe coordinates, for each cell add 1 to every top-left corner
   `(x−dx, y−dy)` with `0 ≤ x−dx ≤ m−k`, `0 ≤ y−dy ≤ n−k`. `count_black_blocks` = Part 2 with k = 2;
   `result[0] = (m−1)(n−1) − len(touched)`. O(|coords|) time and space.
2. Same with `k²` offsets; `result[0] = max(0, m−k+1)·max(0, n−k+1) − #touched`; length `k²+1`.
3. `BlockCounter`: `black` set (idempotency), `per_block` dict (count ≥ 1 only), `hist[1..4]`;
   `paint` moves each touched block from bucket `c` to `c±1`, deleting blocks that return to 0 so
   `counts()[0] = (m−1)(n−1) − len(per_block)` stays right. O(1) per paint and per query.

## Pitfalls hidden tests target
- bucket 0 is arithmetic on ~10^10, not a grid scan; sum of buckets must equal `(m−1)(n−1)`
- last row/column cells touch the blocks above/left of them (corner 1, edge 2, interior 4)
- `m = 2` or `n = 2`; the fully black 2×2 grid → `[0,0,0,0,1]`
- Part 2: `k > min(m, n)` → all zeros of length `k²+1`; `k = 1` → `[white, black]`
- Part 3: idempotent paints; a block dropping back to 0 must leave the map (or bucket 0 is wrong)

## Complexity & measured cost
Part 1 O(c), Part 2 O(c·k²), Part 3 O(1)/op, all O(c) memory (c = black cells). Measured: 0.12 s for
the perf test (10^4 cells on 10^5×10^5: Part 1, Part 2 with k = 5, 2·10^4 streaming paints, one script
run); script run alone 0.03 s, ~25 MB. Budget 2 s / 256 MB.

## Test inventory
15 tests — part1: 9 (incl. 1 io, 1 fmt, 1 perf) · part2: 3 · part3: 3; edge 6.

## Skills exercised
A13 grid/hash counting · S04 group-by aggregation · S13 boundary discipline · S19 incremental design · S21 dict fluency

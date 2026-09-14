---
nodes: [toolbox.hash, performance.memory]
tags: [stripe-oa, qa11, leetcode]
---
# Drill: count sparse-grid blocks by their black-cell count, without building the grid

Forty-five minutes, stdin to stdout. This is LeetCode 2768, Number of Black
Blocks. A grid has `m` rows and `n` columns, all white except for a sparse
list of black cell coordinates; a block is any 2x2 sub-square identified by
its top-left cell. Part 1 returns five counts: how many blocks contain
exactly 0, 1, 2, 3, or 4 black cells. Part 2 generalizes the window to k x k,
returning `k*k + 1` counts. Part 3 turns the batch count into a streaming
`BlockCounter` that supports `paint(x, y, black)` and `counts()`, maintaining
the histogram incrementally rather than recomputing it on every query.

**Constraints to state and honor**
- `m, n` up to 10^5 each (so `m*n` can be ~10^10) but at most 10^4 black
  coordinates — the grid must never be materialized or scanned.
- Coordinates may arrive duplicated; treat duplicates as a single black
  cell.
- A corner cell touches 1 block, an edge cell touches 2, an interior cell
  touches 4 — cells in the last row or column only touch blocks above or to
  their left.
- Part 2: `k > min(m, n)` yields all zeros of length `k*k + 1`; `k = 1`
  degenerates to `[white cells, black cells]`.
- Part 3: `paint` is idempotent — painting an already-black cell black, or
  an already-white cell white, changes nothing.

**Grading points**
- Iterate the black cells, not the grid: for each black cell, add one to
  every valid top-left block corner it belongs to in a hash map, then read
  off buckets 1..4 (or 1..k*k) from that map's values.
- Bucket 0 must come from arithmetic — `(m-1)*(n-1) - (number of touched
  blocks)` — never from iterating untouched blocks, since that count can
  be ~10^10.
- Part 3 needs two things kept in sync: a per-block count map (holding only
  blocks with count >= 1) and the five-bucket histogram, updated by moving
  each of a cell's touched blocks from bucket `c` to `c+1` or `c-1` on every
  paint — both in O(1) amortized per call.
- A block whose count returns to 0 must be dropped from the per-block map
  (or otherwise handled), or bucket 0's derived count goes wrong on the
  next query.
- State explicitly why this is the sparse-event pattern (iterate events,
  hash the windows they touch) rather than a grid-scan pattern, and why
  that distinction is the whole point of the problem at this scale.
- Edge cases: `m = 2` or `n = 2` (a single row of blocks); a fully black
  2x2 grid; zero black cells; duplicate coordinates; verifying the five (or
  k*k+1) buckets sum to the total block count.

**Source**
- `vault/stripe/qA11_lc2768_number_of_black_blocks/question.md`, `vault/stripe/qA11_lc2768_number_of_black_blocks/solution.md`
- `vault/Quick_Check/problems/qA11_lc2768_number_of_black_blocks/problem.md`, `vault/Quick_Check/problems/qA11_lc2768_number_of_black_blocks/REPORT.md`
- `vault/Quick_Check/study/10-solutions/qA11_lc2768_number_of_black_blocks.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):

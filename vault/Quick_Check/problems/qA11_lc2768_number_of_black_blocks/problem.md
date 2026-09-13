# qA11 · LC 2768 Number of Black Blocks — hash-count touched 2×2 blocks, k×k blocks, streaming updates

**Type:** LeetCode "Stripe" tag (algorithm) · **Stage:** phone screen / OA warm-up · **Last asked:** tag snapshot 2026-07-12 (>6 months bucket)
**Frequency:** tag freq 61.2 (liquidslr All, 2025-06), 67.1 (liquidslr >6mo), 62.5 all / 62.5 >6mo (snehasishroy 2026-07) · 3 tag mirrors · **Confidence:** high (tag data), medium (no dated candidate write-up names it)

LC 2768 · *Number of Black Blocks* · Medium · https://leetcode.com/problems/number-of-black-blocks

## The problem (restated)
A grid has `m` rows and `n` columns; every cell is white except the ones listed in `coordinates`
(`[x, y]` = row `x`, column `y`), which are black. A *block* is any 2×2 sub-square of the grid,
identified by its top-left cell `[x, y]` with `0 ≤ x ≤ m−2`, `0 ≤ y ≤ n−2`. Return a list of five
integers where entry `i` is the number of blocks that contain exactly `i` black cells.
LC limits: `2 ≤ m, n ≤ 10^5`, `0 ≤ len(coordinates) ≤ 10^4`, coordinates are unique and in range.
The grid is far too large to materialise — count only the blocks a black cell touches.

## Context
Radar's velocity heat-maps, Terminal's reader-placement grids and the Sigma "hot cells" reports all
ask the same thing: over a huge sparse grid, how many windows contain 0, 1, 2 … flagged events?
The only viable approach is the sparse one — iterate the *events*, not the grid — and the two natural
production follow-ups are a bigger window (k×k) and live updates (a cell flips and the histogram must
change in O(1), not be recomputed).

## Input (stdin)
```
PART n                 # 1..3
m n                    # grid size
K k                    # Part 2 only, window size
x,y                    # Parts 1–2: one black cell per line (none is fine)
B x,y | W x,y | Q      # Part 3: paint black / paint white / query, one event per line
```
Blank lines are ignored; whitespace around `,` is tolerated.

## Output
* Part 1: one line, the five counts separated by single spaces.
* Part 2: one line, the `k²+1` counts.
* Part 3: one line of five counts per `Q` event, in order.

## Rules
### Part 1 — LC signature  `count_black_blocks(m, n, coordinates) -> list[int]`
For each black cell `(x, y)`, the blocks that contain it have top-left corners `(x−dx, y−dy)` for
`dx, dy ∈ {0, 1}`, kept only when `0 ≤ x−dx ≤ m−2` and `0 ≤ y−dy ≤ n−2` (corners touch 1 block,
edges 2, interior cells 4). Count how many black cells each touched block has in a hash map, then
`result[c] += 1` per touched block and `result[0] = (m−1)(n−1) − #touched`. Duplicate coordinates,
if present, are counted once (dedupe first). O(|coordinates|) time and space; never O(m·n).

### Part 2 — k×k blocks  `count_black_blocks_k(m, n, coordinates, k) -> list[int]`
Same idea with `dx, dy ∈ [0, k)` and top-left corners limited to `0 ≤ x' ≤ m−k`, `0 ≤ y' ≤ n−k`.
Return `k²+1` counts; `result[0] = max(0, m−k+1)·max(0, n−k+1) − #touched`. `k = 2` is Part 1;
`k = 1` gives `[white cells, black cells]`; `k > min(m, n)` → all zeros. O(|coordinates|·k²).

### Part 3 — streaming updates  `BlockCounter(m, n)` with `paint(x, y, black)` and `counts()`
Keep the per-block black count (hash map) **and** the histogram of the five counts, updated
incrementally: painting a white cell black moves each of its ≤ 4 blocks from bucket `c` to `c+1`;
painting a black cell white moves them from `c` to `c−1`. `paint` is idempotent (painting black an
already-black cell, or white an already-white cell, changes nothing). `counts()` returns the
histogram in O(1); `counts()[0]` is derived as `(m−1)(n−1) − (blocks with c ≥ 1)`. `paint` is O(1).

## Worked examples
```
LC ex1  m=3 n=3 coordinates=[[0,0]]                 -> [3, 1, 0, 0, 0]
        4 blocks; only block (0,0) contains the black corner cell
LC ex2  m=3 n=3 coordinates=[[0,0],[1,1],[0,2]]     -> [0, 2, 2, 0, 0]
        block(0,0) has (0,0),(1,1) → 2 ; block(0,1) has (1,1),(0,2) → 2 ; block(1,0) has (1,1) → 1 ;
        block(1,1) has (1,1) → 1
Part 1  m=2 n=2 coordinates=[[0,0],[0,1],[1,0],[1,1]] -> [0, 0, 0, 0, 1]
        m=100000 n=100000 coordinates=[]              -> [9999800001, 0, 0, 0, 0]
        m=4 n=4 coordinates=[[1,1]] (interior)        -> [5, 4, 0, 0, 0]   (9 blocks, 4 touched)
        m=4 n=4 coordinates=[[0,1]] (edge)            -> [7, 2, 0, 0, 0]
Part 2  k=2 -> Part 1 ; m=3 n=3 k=3 coordinates=[[0,0],[1,1],[0,2]] -> [0,0,0,1,0,0,0,0,0,0] (one 3×3
        block with 3 black cells) ; m=3 n=3 k=1 same coordinates -> [6, 3] ; k=4 on 3×3 -> 17 zeros
        m=4 n=4 k=3 coordinates=[[1,1]] -> 4 blocks, all contain (1,1) -> [0, 4, 0, 0, 0, 0, 0, 0, 0, 0]
Part 3  m=3 n=3: paint(0,0,black) → counts [3,1,0,0,0]; paint(1,1,black) → [0,3,1,0,0];
        paint(0,2,black) → [0,2,2,0,0] (= LC ex2); paint(1,1,white) → [2,2,0,0,0];
        paint(1,1,white) again → unchanged
```
stdin for Part 1 ex2:
```
PART 1
3 3
0,0
1,1
0,2
```
→ `0 2 2 0 0`
stdin for Part 3 (`PART 3` / `3 3` / `B 0,0` / `Q` / `B 1,1` / `B 0,2` / `Q` / `W 1,1` / `Q`) →
```
3 1 0 0 0
0 2 2 0 0
2 2 0 0 0
```

## Edge cases hidden tests are known to target
- `result[0]` must come from `(m−1)(n−1)` arithmetic — it can be ~10^10, and the grid must never be built
- corner (1 block), edge (2), interior (4) cells; cells in the last row/column touch blocks *above/left*
- `m = 2` or `n = 2` (a single row of blocks); the fully black 2×2 grid → `[0,0,0,0,1]`
- no black cells → `[(m−1)(n−1), 0, 0, 0, 0]`
- Part 2: `k > min(m, n)` → zero blocks; `k = 1`; output length `k²+1`
- Part 3: idempotent paints; painting white must decrement the *right* buckets; a block whose count
  returns to 0 must count in bucket 0 again (drop it from the map or treat 0 correctly)

## Variants seen in the wild
- LC 2768 itself with the 2×2 block hard-coded; the tag lists only this version.
- "Count windows with at least t hits" over a sparse event grid — Part 2 with a threshold sum.
- Same sparse trick in 1-D: "how many sliding windows contain ≥ t events" (q23 rate limiter style).

## Why Stripe asks it
The whole point is noticing that `m·n` is 10^10 while the events are 10^4 — iterate the events and hash
the windows they touch. That is the sparse-grid instinct Stripe's data-heavy teams rely on, and the
streaming follow-up is the "keep the aggregate up to date, don't recompute" habit of every
dashboard/alerting service.

## Stripe-flavored follow-ups
1. Bigger windows (k×k) — Part 2; discuss O(|cells|·k²) vs a 2-D prefix sum over the *touched* region.
2. Live updates — Part 3 (`paint` in O(1), histogram always ready).
3. Top-t hottest windows after every update — keep a heap or a bucket index on the block counts.

## What this tests
skills: A13 grid/hash counting · S04 group-by aggregation · S13 boundary discipline · S19 incremental design · S21 stdlib fluency (dict/Counter)

## Sources
- https://leetcode.com/problems/number-of-black-blocks
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/5.%20All.csv (freq 61.2)
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/4.%20More%20Than%20Six%20Months.csv (freq 67.1)
- https://raw.githubusercontent.com/snehasishroy/leetcode-companywise-interview-questions/master/stripe/all.csv (freq 62.5 all / 62.5 >6mo)
- catalog/raw/github_repos.md §30 (tag table, freq 61.2)

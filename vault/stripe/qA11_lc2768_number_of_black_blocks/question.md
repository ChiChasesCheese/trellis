# qA11 · LC 2768 Number of Black Blocks — hash-count touched 2×2 blocks, k×k blocks, streaming updates

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

## 关联知识点

- [[a13-grid-hash-counting|A13 网格 / 哈希计数]]
- [[s04-group-then-aggregate|S04 分组聚合，规则每组一次而不是每行一次]]
- [[s13-closed-intervals-offbyone|S13 闭区间、补齐空隙、off-by-one 纪律]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
- [[s21-python-stdlib-fluency|S21 语言熟练度与标准库]]

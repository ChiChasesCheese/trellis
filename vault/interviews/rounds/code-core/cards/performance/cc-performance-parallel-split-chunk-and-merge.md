---
id: cc-performance-parallel-split-chunk-and-merge
node: performance.parallel-split
type: qa
---
## Q
Find the K largest cells of a large grid, split across workers. How do you split it, what does each worker send back, and why is merging correct?

## A
**Each worker gets a band of whole rows and returns only its own top K. The answer is the top K of those w · K candidates.**

```python
from concurrent.futures import ProcessPoolExecutor
import heapq

def band_top_k(args):
    rows, r0, k = args                 # a band of rows starting at row r0
    cells = ((v, r0 + i, j) for i, row in enumerate(rows)
             for j, v in enumerate(row))
    return heapq.nlargest(k, cells)    # O(cells * log k)

def grid_top_k(grid, k, workers=4):
    m = len(grid)
    w = max(1, min(workers, m))
    bands = [(grid[m * i // w: m * (i + 1) // w], m * i // w, k)
             for i in range(w)]
    with ProcessPoolExecutor(max_workers=w) as ex:
        partials = list(ex.map(band_top_k, bands))
    # global top-k is inside the union of local top-k lists
    return heapq.nlargest(k, (c for p in partials for c in p))
```

- **Why correct.** If a global winner were not in its band's top K, K cells of that band would beat it — contradiction.
- **Why row bands.** One contiguous slice: cheap to cut and send, read in memory order.
- **Ties.** `(value, row, col)` tuples give a total order, so parallel equals serial exactly.
- **Uneven work.** Cut 4 × w chunks; idle workers take the extras.
- **Complexity.** O(m·n·log K / w) per worker, O(w·K·log K) merge; only w·K tuples travel back.

**Follow-ups.** K nearest neighbours: same pattern, key `-distance`. Workers on a 2D mesh that only talk to neighbours: merge in a tree, log2(w) rounds.

## Q zh
找出一个大网格里最大的 K 个格子，网格分给多个 worker。怎么切？每个 worker 返回什么？为什么合并是正确的？

## A zh
**每个 worker 分一段完整的行（band），只返回自己的前 K 个。答案是这 w · K 个候选里的前 K 个。**

```python
from concurrent.futures import ProcessPoolExecutor
import heapq

def band_top_k(args):
    rows, r0, k = args                 # a band of rows starting at row r0
    cells = ((v, r0 + i, j) for i, row in enumerate(rows)
             for j, v in enumerate(row))
    return heapq.nlargest(k, cells)    # O(cells * log k)

def grid_top_k(grid, k, workers=4):
    m = len(grid)
    w = max(1, min(workers, m))
    bands = [(grid[m * i // w: m * (i + 1) // w], m * i // w, k)
             for i in range(w)]
    with ProcessPoolExecutor(max_workers=w) as ex:
        partials = list(ex.map(band_top_k, bands))
    # global top-k is inside the union of local top-k lists
    return heapq.nlargest(k, (c for p in partials for c in p))
```

- **为什么正确。** 如果某个全局赢家不在自己那段的前 K 里，那段就有 K 个格子比它大——矛盾。
- **为什么按行分段。** 一段是一块连续切片：切和发都便宜，按内存顺序读。
- **平局。** `(value, row, col)` 元组给出全序，并行结果与串行完全相同。
- **工作量不均。** 切成 4 × w 块；空闲的 worker 接走多出来的。
- **复杂度。** 每个 worker O(m·n·log K / w)，合并 O(w·K·log K)；只传回 w·K 个元组。

**追问。** K 个最近邻：同一模式，键用 `-distance`。worker 排成二维网格、只能和邻居通信：按树形两两合并，log2(w) 轮。

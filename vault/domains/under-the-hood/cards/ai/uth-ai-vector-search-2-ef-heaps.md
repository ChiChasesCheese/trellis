---
id: uth-ai-vector-search-2-ef-heaps
node: ai.vector-search
type: qa
step: 2
---
## Q
**ef_search 到底是什么**｜pgvector · 0.8.0 HNSW

到了底层，为什么不能顺着一条路走到底？`hnsw.ef_search`（默认 40）控制的是什么？

## A
**背景。** 只走一条路，容易停在一个比所有邻居都近、却不是全局最近的点上。所以底层同时盯着一批候选，而不是一个点。

**结构。** 两个堆（heap）加一个已访问集合：

- 候选堆（最小堆）：待探索的点，离查询最近的先取出，去看它的邻居
- 结果堆（最大堆）：目前最好的 `ef` 个，堆顶是其中最远的，新点更近就把它顶掉
- 已访问集合：每个点只算一次距离

**细节。**

- 停止条件：候选堆里最近的点，已经比结果堆里最远的还远，再走不会更好
- `hnsw.ef_search` 默认 40，范围 1 到 1000：调大召回更高、查询更慢

**坑。** 返回行数最多就是 `ef_search`，`LIMIT 100` 配默认值拿不到 100 行；`WHERE` 过滤发生在索引扫描之后，只有 10% 的行满足条件时，40 个候选里平均只剩 4 行。

**例题：** LC 778 水位上升的泳池中游泳（同样是堆里永远先取「当前最优」的格子，配一个已访问集合）

`n x n` 的网格，`grid[i][j]` 是平台高度，时间 `t` 时水位为 `t`，只能在水位不低于两端高度时游到相邻平台；求从左上角到右下角的最少时间。例：`[[0,2],[1,3]]` → `3`。

```python
from heapq import heappop, heappush


def swim_in_water(grid: list[list[int]]) -> int:
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]                    # (到达此格所需的最低水位, 行, 列)
    seen = {(0, 0)}
    while heap:
        t, x, y = heappop(heap)                    # 弹出的是"当前最低水位下能到的最低一格"
        if x == y == n - 1:
            return t
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in seen:
                seen.add((nx, ny))
                heappush(heap, (max(t, grid[nx][ny]), nx, ny))
    return -1
```

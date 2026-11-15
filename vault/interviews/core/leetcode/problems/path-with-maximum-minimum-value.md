---
slug: path-with-maximum-minimum-value
---
## Q
**LC 1102 得分最高的路径**｜Medium

`m × n` 的整数网格，从左上角 `(0, 0)` 走到右下角，每步向四个方向之一。路径的得分是路径上所有数的最小值，求所有路径中得分最大的。

## A
**一句话。** 类 Dijkstra：用最大堆总是扩展当前最大的格子，到达终点时，路径上遇到的最小值就是答案；最优路径的瓶颈（最小值）只会随扩展不断变小。

```python
def maximum_minimum_path(grid):
    m, n = len(grid), len(grid[0])
    heap = [(-grid[0][0], 0, 0)]       # 最大堆：存相反数
    seen = {(0, 0)}
    best = grid[0][0]
    while heap:
        v, i, j = heappop(heap)
        best = min(best, -v)           # 路径的最小值
        if (i, j) == (m - 1, n - 1):
            return best
        for x, y in ((i + 1, j), (i - 1, j),
                     (i, j + 1), (i, j - 1)):
            if (0 <= x < m and 0 <= y < n
                    and (x, y) not in seen):
                seen.add((x, y))
                heappush(heap, (-grid[x][y], x, y))
```

**复杂度。** 时间 `O(mn log mn)`，空间 `O(mn)`。

**易错点。**
- 用最小堆：要的是尽量大的最小值，应优先扩展大的格子。
- 起点不计入答案：起点和终点的值也在路径上，`best` 要从起点的值开始。
- 出堆才标记已访问：入堆就标记，避免重复入堆。

**追问。**
- 二分答案怎么做？：对阈值 `t` 用 BFS 判断只经过 `≥ t` 的格子能否到终点，`O(mn log V)`。
- 并查集呢？：按值从大到小激活格子并合并邻居，起点与终点第一次连通时的值就是答案。

**同模式。** LC 1631 最小体力消耗路径、LC 778 水位上升的泳池中游泳、LC 743 网络延迟时间、LC 1584 连接所有点的最小费用

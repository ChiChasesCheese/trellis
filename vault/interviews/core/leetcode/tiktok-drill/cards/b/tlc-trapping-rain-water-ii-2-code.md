---
id: tlc-trapping-rain-water-ii-2-code
node: b.trapping-rain-water-ii
type: qa
step: 2
---
## Q
**LC 407 接雨水 II**｜写出 Python 实现

`heightMap` 是 `m × n`（`1 <= m, n <= 200`，高度 `0` 到 `2 * 10^4`）。水只能沿上下左右流动，流出边界即消失。返回最多能存的水的体积。

## A
**思路。** 把最外圈所有格子放进小根堆，元素是 `(水位, 行, 列)`，外圈水位就是自身高度。每次弹出水位最低的格子，检查它的未访问邻居：邻居能存的水是 `max(0, 当前水位 − 邻居高度)`；邻居入堆时的水位是 `max(当前水位, 邻居高度)`。

```python
import heapq

def trap_rain_water(height_map: list[list[int]]) -> int:
    m, n = len(height_map), len(height_map[0])
    if m < 3 or n < 3:
        return 0                               # 没有内部格子，存不住水
    seen = [[False] * n for _ in range(m)]
    heap: list[tuple[int, int, int]] = []      # (当前水位, 行, 列)：最外圈先入堆作为「围墙」
    for r in range(m):
        for c in range(n):
            if r in (0, m - 1) or c in (0, n - 1):
                heap.append((height_map[r][c], r, c))
                seen[r][c] = True
    heapq.heapify(heap)
    water = 0
    while heap:
        level, r, c = heapq.heappop(heap)      # 目前围墙里最矮的一格：它的水位决定了邻居的水位
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and not seen[nr][nc]:
                seen[nr][nc] = True
                water += max(0, level - height_map[nr][nc])
                heapq.heappush(heap, (max(level, height_map[nr][nc]), nr, nc))
    return water
```

运行：`[[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]` → `4`，`[[3,3,3,3,3],[3,2,2,2,3],[3,2,1,2,3],[3,2,2,2,3],[3,3,3,3,3]]` → `10`，`[[5]]` → `0`，`[[1,2],[3,4]]` → `0`，`[[1,1,1],[1,0,1],[1,1,1]]` → `1`。

**复杂度。** 时间 `O(mn log(mn))`：每格入堆、出堆一次，堆操作 `O(log(mn))`；空间 `O(mn)`：`seen` 和堆。

**写法要点。** 元组 `(水位, 行, 列)` 直接放进 `heapq`，按水位排序，水位相同时再按坐标，不会比较失败；先用列表收集外圈再 `heapify`，比逐个 `heappush` 快；入堆的是「有效水位」`max(level, h)`，不是原始高度，这是本算法的核心；外圈格子入堆时就标记 `seen`，避免被内部格子重复加入。

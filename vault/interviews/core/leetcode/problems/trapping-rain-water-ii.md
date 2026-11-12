---
slug: trapping-rain-water-ii
---
## Q
**LC 407 接雨水 II**｜Hard

给 `m × n` 的高度图，求下雨后最多能存多少水（水只往上下左右流，流出边界就没了）。

## A
**一句话。** 木桶原理加最小堆：最外圈入堆当围墙，每次取最矮的一格，用它的水位去灌未访问的邻居。

```python
def trap_rain_water(h):
    m, n = len(h), len(h[0])
    seen = [[False] * n for _ in range(m)]
    heap = []     # (水位, 行, 列)
    for r in range(m):
        for c in range(n):
            if r in (0, m - 1) or c in (0, n - 1):
                heap.append((h[r][c], r, c))
                seen[r][c] = True
    heapq.heapify(heap)
    water = 0
    while heap:
        level, r, c = heapq.heappop(heap)  # 最矮的围墙
        for x, y in (r+1, c), (r-1, c), (r, c+1), (r, c-1):
            if 0 <= x < m and 0 <= y < n and not seen[x][y]:
                seen[x][y] = True
                water += max(0, level - h[x][y])
                top = max(level, h[x][y])
                heapq.heappush(heap, (top, x, y))
    return water
```

**复杂度。** 时间 `O(mn log(mn))`，空间 `O(mn)`。

**易错点。**
- 邻居入堆用自己的高度而不是 `max(level, 高度)`：水位被低估，示例 2 得 `2`，应为 `10`。
- 用行列最大值的较小者推广一维解：水能绕路从缺口流出，示例 1 得 `5`，应为 `4`。

**追问。**
- 为什么先处理最矮的围墙？：它是当前木桶的短板，邻居的水位不可能超过它。
- 水能斜着流怎么改？：邻居换成 8 个方向，其余不变。

**同模式。** LC 42 接雨水、LC 778 水位上升的泳池中游泳、LC 1631 最小体力消耗路径、LC 743 网络延迟时间

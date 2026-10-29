---
id: tlc-trapping-rain-water-ii-4-followup
node: a.trapping-rain-water-ii
type: qa
step: 4
---
## Q
**LC 407 接雨水 II**｜追问

面试官接着问：（1）还要返回每个格子的水深？（2）水也可以沿对角线流动（八个方向）？（3）一维版本（LC 42）为什么不用堆，怎么做到 `O(1)` 空间？

## A
1. **每格水深**：入堆时已经算出水位，记录到二维数组即可。
```python
import heapq

def water_depth(height_map: list[list[int]]) -> list[list[int]]:
    m, n = len(height_map), len(height_map[0])
    depth = [[0] * n for _ in range(m)]
    seen = [[False] * n for _ in range(m)]
    heap = [(height_map[r][c], r, c) for r in range(m) for c in range(n)
            if r in (0, m - 1) or c in (0, n - 1)]
    for _, r, c in heap:
        seen[r][c] = True
    heapq.heapify(heap)
    while heap:
        level, r, c = heapq.heappop(heap)
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and not seen[nr][nc]:
                seen[nr][nc] = True
                depth[nr][nc] = max(0, level - height_map[nr][nc])
                heapq.heappush(heap, (max(level, height_map[nr][nc]), nr, nc))
    return depth
```
示例 2 返回 `[[0,0,0,0,0],[0,1,1,1,0],[0,1,2,1,0],[0,1,1,1,0],[0,0,0,0,0]]`，总和 `10`。
2. **八方向**：邻居列表换成 8 个方向，算法不变，水位定义依然是到边界路径的最高点最小值。
3. **一维 LC 42**：一维中，左右两个出口把「路径」限制成只有两条（向左、向右），水位是 `min(左侧最高, 右侧最高)`，不需要堆。双指针从两端向中间走，每步移动较矮的一侧并累加，`O(n)` 时间、`O(1)` 空间。二维里出口是整个外圈，且路径可以拐弯，这个简化不再成立。

**Python 提醒**：`heapq` 里的元素是元组时，水位相同会继续比较第二、三项（行、列），这里都是整数所以安全；如果元组里放了不能比较的对象（如自定义类、`None`），水位相同时会抛 `TypeError`，需要加一个递增计数器作为第二项。

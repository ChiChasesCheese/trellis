---
id: tlc-swim-in-rising-water-2-code
node: a.swim-in-rising-water
type: qa
step: 2
---
## Q
**LC 778 水位上升的泳池中游泳**｜写出 Python 实现

`n x n` 矩阵 `grid`（`1 <= n <= 50`，`0 <= grid[i][j] < n^2`，高度互不相同），时间 `t` 时水位为 `t`，相邻平台在水位不低于两者高度时可通行，从 `(0, 0)` 到 `(n-1, n-1)` 最少需要多少时间。

## A
**思路。** 堆元素是 `(到达此格所需的最低水位, 行, 列)`，起点键是它自己的高度。每次弹出键最小的格子；终点出堆就返回。否则把没入过堆的邻格以 `max(当前键, 邻格高度)` 入堆。

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

运行：`[[0,2],[1,3]]` → `3`；`5 x 5` 的示例 → `16`；`[[0]]` → `0`；`[[3,0],[1,2]]` → `3`。

**复杂度。** 时间 `O(n^2 log n)`：`n^2` 个格子各入堆、出堆一次；空间 `O(n^2)`：`seen` 和堆。

**写法要点。** 堆里放三元组 `(键, x, y)`，`heapq` 按元组字典序比较，键相同时比较坐标，不会报错；`x == y == n - 1` 一次判断「到达右下角」；入堆时就标记 `seen`，因为第一次到达某格时的键已经是它的最小值（后弹出的键只会更大）；`dx, dy` 用四个元组写出，避免嵌套循环。

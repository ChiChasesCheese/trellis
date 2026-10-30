---
id: tlc-pacific-atlantic-water-flow-2-code
node: p4.pacific-atlantic-water-flow
type: qa
step: 2
---
## Q
**LC 417 太平洋大西洋水流问题**｜写出 Python 实现

`heights` 是 `m × n`（`1 <= m, n <= 200`，值 `0` 到 `10^5`）。太平洋靠左、上边界，大西洋靠右、下边界，水可以流向高度小于等于当前格的上下左右邻居。返回所有既能流向太平洋、又能流向大西洋的格子 `[r, c]`。

## A
**思路。** 定义 `flood(起点列表)`：从起点开始 BFS，只走向高度不低于当前格的邻居，返回访问到的格子集合。对太平洋，起点是第一行和第一列；对大西洋，起点是最后一行和最后一列。两个集合求交集。

```python
from collections import deque

def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    m, n = len(heights), len(heights[0])

    def flood(starts: list[tuple[int, int]]) -> set[tuple[int, int]]:
        seen = set(starts)                     # 从海洋出发，逆流而上：只走向不矮于当前格的邻居
        queue = deque(starts)
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen and heights[nr][nc] >= heights[r][c]:
                    seen.add((nr, nc))
                    queue.append((nr, nc))
        return seen

    pacific = flood([(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)])
    atlantic = flood([(m - 1, c) for c in range(n)] + [(r, n - 1) for r in range(m - 1)])
    return [[r, c] for r, c in sorted(pacific & atlantic)]
```

运行：示例 1 → `[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]`，示例 2 `[[2,1],[1,2]]` → `[[0,0],[0,1],[1,0],[1,1]]`，`[[1]]` → `[[0,0]]`，`[[1,1]]` → `[[0,0],[0,1]]`，`[[1,1],[1,1]]` → 四个格子全部。

**复杂度。** 时间 `O(mn)`：每次 `flood` 每格最多入队一次，两次 `flood` 加交集；排序 `O(k log k)`（`k` 是答案个数，仅为输出整齐，可省）；空间 `O(mn)`。

**写法要点。** `flood` 做成内层函数，共享 `heights`、`m`、`n`；`seen` 同时兼任访问标记和返回值，起点直接 `set(starts)`；集合交集用 `pacific & atlantic`，比两层循环对比简洁；元组 `(r, c)` 可哈希，适合放集合；起点列表里用 `range(1, m)` / `range(m - 1)` 避免左上、右下角重复（重复也无害，因为 `seen` 去重）。

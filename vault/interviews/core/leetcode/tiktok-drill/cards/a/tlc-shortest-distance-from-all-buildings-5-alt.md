---
id: tlc-shortest-distance-from-all-buildings-5-alt
node: a.shortest-distance-from-all-buildings
type: qa
step: 5
---
## Q
**LC 317 离建筑物最近的距离**｜另一种解法

不从建筑出发，改成从每块空地出发做 BFS，数能找到几幢建筑并累加距离。写出来，并说明什么时候选它。

## A
**思路。** 对每块空地 BFS：扩展时只进入 `0` 的格子；遇到建筑（`1`）就记下距离并计数，但不继续穿过去。如果找到的建筑数等于总数，这块空地合格，用累加的距离更新答案。

```python
from collections import deque

def shortest_distance_from_empty(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    buildings = sum(row.count(1) for row in grid)
    best = -1
    for sr in range(m):
        for sc in range(n):
            if grid[sr][sc] != 0:
                continue
            seen = {(sr, sc)}
            queue = deque([(sr, sc, 0)])
            found = total = 0
            while queue:
                r, c, d = queue.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        if grid[nr][nc] == 1:
                            found += 1         # 建筑：记距离，但不能穿过去
                            total += d + 1
                        elif grid[nr][nc] == 0:
                            queue.append((nr, nc, d + 1))
            if found == buildings and (best == -1 or total < best):
                best = total
    return best
```

运行：`[[1,0,2,0,1],[0,0,0,0,0],[0,0,1,0,0]]` → `7`，`[[1,0]]` → `1`，`[[1]]` → `-1`，`[[1,0,2,1]]` → `-1`。

**对比。** 两种做法都是 `O(mn)` 的 BFS 重复多次：从建筑出发是 `B` 次，从空地出发是 `E` 次（`E` 为空地数）。**谁少就从谁出发**：建筑少、空地多时选主解法；建筑多、空地少时选这个。两者在最坏情形（建筑和空地各占一半）下都是 `O((mn)^2)` 量级，`50 × 50` 时约 `10^6 ~ 10^7`，都能通过。

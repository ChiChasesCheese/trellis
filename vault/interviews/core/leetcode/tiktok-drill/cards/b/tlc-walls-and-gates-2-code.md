---
id: tlc-walls-and-gates-2-code
node: b.walls-and-gates
type: qa
step: 2
---
## Q
**LC 286 墙与门**｜写出 Python 实现

`rooms` 是 `m × n` 网格（`1 <= m, n <= 250`），值为 `-1`（墙）、`0`（门）、`INF = 2147483647`（空房间）。原地把每个空房间填成到最近的门的步数；走不到门则保持 `INF`。不返回值。

## A
**思路。** 先把所有门放进队列。每次取出一个格子，看它的上下左右：邻居在网格内且仍是 `INF`，说明还没被填过，就填成当前格子的值加一并入队。BFS 按层推进，所以第一次填入的就是最短距离。

```python
from collections import deque

INF = 2**31 - 1

def walls_and_gates(rooms: list[list[int]]) -> None:
    m, n = len(rooms), len(rooms[0])
    queue = deque((r, c) for r in range(m) for c in range(n) if rooms[r][c] == 0)  # 所有门同时入队
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and rooms[nr][nc] == INF:   # 还没被填过的空房间
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
```

运行：示例 1 → `[[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]`；`[[-1]]` → `[[-1]]`；`[[INF]]` → `[[INF]]`；`[[0]]` → `[[0]]`；`250 × 250` 空网格、对角两个门 → 中心格子 `248`。

**复杂度。** 时间 `O(mn)`：每格入队一次，每次检查 `4` 个方向；空间 `O(mn)`：队列最坏装下一整层波前。

**写法要点。** 用生成器表达式直接构造初始队列，不用先建列表；`INF` 既是「未访问」标记，又是「空房间」的值，省掉额外的 `visited` 矩阵；方向元组写在循环里，比 `dirs = [(1,0),...]` 少一层间接；链式比较 `0 <= nr < m` 比 `nr >= 0 and nr < m` 更短也更不容易写错。

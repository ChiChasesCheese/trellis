---
id: tlc-patterns-graph-traversal-6-implicit-graph
node: patterns.graph-traversal
type: qa
step: 6
---
## Q
**图与网格的 BFS / DFS｜多源与隐式图：最短的桥、墙与门、单词接龙、二分图染色**

这些题的"图"藏在哪里？BFS 怎么改？

## A
**LC 934 最短的桥**：先 DFS 找到第一座岛，把它**整体**作为多源 BFS 的起点，向外一层层扩展，碰到另一座岛即返回步数。

```python
from collections import deque
def shortest_bridge(grid: list[list[int]]) -> int:
    n = len(grid)
    q: deque[tuple[int, int]] = deque()
    start = next((r, c) for r in range(n) for c in range(n) if grid[r][c] == 1)
    grid[start[0]][start[1]] = 2
    stack = [start]
    while stack:                           # 第一座岛：标成 2 并入队
        x, y = stack.pop()
        q.append((x, y))
        for a, b in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= a < n and 0 <= b < n and grid[a][b] == 1:
                grid[a][b] = 2
                stack.append((a, b))
    steps = 0
    while q:
        for _ in range(len(q)):
            x, y = q.popleft()
            for a, b in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= a < n and 0 <= b < n:
                    if grid[a][b] == 1:
                        return steps       # 碰到另一座岛：steps 个水格被翻转
                    if grid[a][b] == 0:
                        grid[a][b] = 2
                        q.append((a, b))
        steps += 1
    return -1
print(shortest_bridge([[0,1],[1,0]]), shortest_bridge([[0,1,0],[0,0,0],[0,0,1]]))   # 1 2
```

**LC 286 墙与门**：所有门（值 0）同时入队，向空房间扩散，写入距离；每个房间只会被最近的门首次到达。

**LC 127 单词接龙（隐式图）**：节点是单词，边是「只差一个字母」。为避免 `O(N^2)` 两两比较，建「通配符桶」：`"hot"` 对应 `"*ot"`、`"h*t"`、`"ho*"`，同一桶里的单词互为邻居。BFS 层数 + 1 即答案。

**LC 815 公交路线**：节点取**路线**而不是车站；车站 → 经过它的路线集合，BFS 的单位是"换乘一次"。

**LC 886 可能的二分法**：BFS / DFS 染色，邻居必须异色，冲突即返回 `False`；图可能不连通，要从每个未染色的点出发。

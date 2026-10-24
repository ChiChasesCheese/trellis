---
id: tlc-patterns-topo-sort-7-matrix-path
node: patterns.topo-sort
type: qa
step: 7
---
## Q
**拓扑排序（Topological Sort）｜矩阵中的最长递增路径（LC 329）**

矩阵里怎样用拓扑排序求最长递增路径？为什么递归加 `@cache` 在最大数据上会失败？

## A
**LC 329 矩阵中的最长递增路径**：把每个格子连向比它大的邻居，得到 DAG，最长路径就是 DAG 上的最长链。递归 + `@cache` 很短，但 `200 x 200` 的蛇形矩阵递归深度可达 `40000`，Python 会 `RecursionError`；用 Kahn 的"分层剥洋葱"，从出度为 0 的格子（局部最大值）开始往回剥，层数就是答案：

```python
from collections import deque
def longest_increasing_path(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    out = [[sum(1 for dr, dc in dirs if 0 <= r + dr < m and 0 <= c + dc < n
                and matrix[r + dr][c + dc] > matrix[r][c]) for c in range(n)] for r in range(m)]
    q = deque((r, c) for r in range(m) for c in range(n) if out[r][c] == 0)
    layers = 0
    while q:
        layers += 1
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in dirs:
                a, b = r + dr, c + dc
                if 0 <= a < m and 0 <= b < n and matrix[a][b] < matrix[r][c]:
                    out[a][b] -= 1
                    if out[a][b] == 0:
                        q.append((a, b))
    return layers
print(longest_increasing_path([[9,9,4],[6,6,8],[2,1,1]]), longest_increasing_path([[3,4,5],[3,2,6],[2,2,1]]), longest_increasing_path([[1]]))   # 4 4 1
```

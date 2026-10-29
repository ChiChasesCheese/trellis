---
id: tlc-01-matrix-2-code
node: b.01-matrix
type: qa
step: 2
---
## Q
**LC 542 01 矩阵**｜写出 Python 实现

`m x n` 的 0/1 矩阵 `mat`（`1 <= m * n <= 10^4`，至少有一个 `0`），返回每个格子到最近的 `0` 的距离，相邻格子距离为 1。

## A
**思路。** 多源 BFS：先把所有 `0` 入队并把它们的距离置 0；然后逐个弹出格子，给还没访问的上下左右邻居赋值 `dist + 1` 并入队。先被赋值的一定是最短的，所以每个格子只处理一次。

```python
from collections import deque
from itertools import pairwise


def update_matrix(mat: list[list[int]]) -> list[list[int]]:
    m, n = len(mat), len(mat[0])
    dist = [[-1] * n for _ in range(m)]            # -1 表示还没访问
    queue: deque[tuple[int, int]] = deque()
    for i, row in enumerate(mat):
        for j, value in enumerate(row):
            if value == 0:
                dist[i][j] = 0
                queue.append((i, j))               # 所有 0 一起作为第 0 层
    while queue:
        i, j = queue.popleft()
        for di, dj in pairwise((1, 0, -1, 0, 1)):  # 依次得到 (1,0) (0,-1) (-1,0) (0,1) 四个方向
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and dist[ni][nj] == -1:
                dist[ni][nj] = dist[i][j] + 1      # 入队时就标记，保证每格只入队一次
                queue.append((ni, nj))
    return dist
```

运行：`[[0,0,0],[0,1,0],[0,0,0]]` → `[[0,0,0],[0,1,0],[0,0,0]]`，`[[0,0,0],[0,1,0],[1,1,1]]` → `[[0,0,0],[0,1,0],[1,2,1]]`，`[[0,1,1,1,0]]` → `[[0,1,2,1,0]]`，`[[0]]` → `[[0]]`，`1 行 10000 列、只有左端是 0 时最右格` → `9999`，`100x100、只有左上角是 0 时最右下格` → `198`。

**复杂度。** 时间 `O(mn)`；空间 `O(mn)`。

**写法要点。** `deque.popleft()` 是 `O(1)`，`list.pop(0)` 是 `O(n)`；`pairwise((1, 0, -1, 0, 1))` 用一个常量序列生成四个方向，省去手写方向表；`[[-1] * n for _ in range(m)]` 每行都是独立的列表，不能写成 `[[-1] * n] * m`；`dist` 兼任访问标记，不需要额外的 `visited`。

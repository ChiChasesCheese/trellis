---
id: tlc-longest-increasing-path-in-a-matrix-2-code
node: b.longest-increasing-path-in-a-matrix
type: qa
step: 2
---
## Q
**LC 329 矩阵中的最长递增路径**｜写出 Python 实现

整数矩阵 `matrix`（`1 <= m, n <= 200`，值 `0..2^31 - 1`），每步可上下左右移动，路径上的值严格递增。写 `longest_increasing_path(matrix)`，返回最长递增路径的格子数。要求不会因为路径很长而递归溢出。

## A
**思路。** 先算每个格子的出度（比它大的邻居个数）；出度为 `0` 的格子是第一层；每剥一层，把比它们小的邻居出度减一，减到 `0` 的进入下一层；层数就是答案。

```python
from itertools import product


def longest_increasing_path(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    out_deg = [[0] * n for _ in range(m)]      # 比自己大的邻居个数 = 出边数
    for i, j in product(range(m), range(n)):
        for di, dj in dirs:
            x, y = i + di, j + dj
            if 0 <= x < m and 0 <= y < n and matrix[x][y] > matrix[i][j]:
                out_deg[i][j] += 1
    layer = [(i, j) for i, j in product(range(m), range(n)) if out_deg[i][j] == 0]
    steps = 0                                  # 剥掉的层数 = 最长路径的点数
    while layer:
        steps += 1
        next_layer: list[tuple[int, int]] = []
        for i, j in layer:
            for di, dj in dirs:
                x, y = i + di, j + dj
                if 0 <= x < m and 0 <= y < n and matrix[x][y] < matrix[i][j]:
                    out_deg[x][y] -= 1         # 它的一个“更大邻居”已被剥掉
                    if out_deg[x][y] == 0:
                        next_layer.append((x, y))
        layer = next_layer
    return steps
```

运行：`[[9,9,4],[6,6,8],[2,1,1]]` → `4`，`[[3,4,5],[3,2,6],[2,2,1]]` → `4`，`[[1]]` → `1`，`[[5,5],[5,5]]` → `1`；`200 x 200` 蛇形严格递增矩阵 → `40000`。

**复杂度。** 时间 `O(mn)`：算出度和剥层各看每格的 `4` 个邻居一次；空间 `O(mn)`：出度表加当前层 / 下一层。

**写法要点。** `dirs` 提到循环外作为元组常量；`itertools.product(range(m), range(n))` 把双层循环写成一层，列表推导里也能用。`layer` / `next_layer` 两个列表按层交替，比单个 `deque` 加计数更清楚，层数就是 `steps`。出度为 `0` 的判断放在减一之后，保证每个格子只进队一次。矩阵值可以到 `2^31 - 1`，Python 整数没有溢出问题，只比较大小。

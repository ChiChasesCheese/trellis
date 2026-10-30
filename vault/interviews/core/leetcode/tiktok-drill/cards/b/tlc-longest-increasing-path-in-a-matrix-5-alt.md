---
id: tlc-longest-increasing-path-in-a-matrix-5-alt
node: b.longest-increasing-path-in-a-matrix
type: qa
step: 5
---
## Q
**LC 329 矩阵中的最长递增路径**｜另一种解法

不用递归的做法是什么？它为什么不怕路径很长，什么时候选它、什么时候选记忆化 DFS？

## A
**思路。** 「相邻且更大」的边构成 DAG，用拓扑排序（Kahn 算法）按层剥洋葱。先算每个格子的出度（比它大的邻居个数）；出度为 `0` 的格子是第一层；每剥一层，把比它们小的邻居出度减一，减到 `0` 的进入下一层；层数就是最长路径的格子数。

```python
from itertools import product


def longest_increasing_path_topo(matrix: list[list[int]]) -> int:
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

运行：`[[9,9,4],[6,6,8],[2,1,1]]` → `4`，`[[3,4,5],[3,2,6],[2,2,1]]` → `4`，`[[1]]` → `1`，`[[5,5],[5,5]]` → `1`；`200 x 200` 的蛇形严格递增矩阵 → `40000`；`200 x 200` 的梳状矩阵（最长路径 `20101` 格）→ `20101`，没有 `RecursionError`。

**复杂度。** 时间 `O(mn)`：算出度和剥层各看每格的 `4` 个邻居一次；空间 `O(mn)`：出度表加当前层 / 下一层。

**为什么不怕路径长。** 全程是循环，层与层之间靠列表交替，没有调用栈，深度只体现在层数上，不受递归上限影响。

**取舍。**
- 记忆化 DFS：代码最短，状态定义最贴近题意，面试里先写它；路径不长时没有问题。
- 拓扑排序：全程迭代，路径可能长达两万格时更稳；多一次算出度的预处理，逻辑也比「缓存递归」绕一点。
- 面试里可以先写记忆化 DFS，并主动指出「路径可能长达两万格，Python 默认递归深度不够，`@cache` 还会撞 C 栈上限」，再换成拓扑排序或排序 DP。

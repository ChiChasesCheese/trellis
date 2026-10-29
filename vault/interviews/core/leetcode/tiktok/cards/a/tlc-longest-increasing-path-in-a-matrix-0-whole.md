---
id: tlc-longest-increasing-path-in-a-matrix-0-whole
node: a.longest-increasing-path-in-a-matrix
type: qa
---
## Q
**LC 329 矩阵中的最长递增路径**｜Hard · TikTok·字节 高频

给一个 `m x n` 的整数矩阵 `matrix`，求其中**最长递增路径**的长度（路径上的格子数）。每一步可以向上、下、左、右移动一格，不能走对角线，不能走出边界，路径上的值必须严格递增。`m == matrix.length`，`n == matrix[i].length`，`1 <= m, n <= 200`，`0 <= matrix[i][j] <= 2^31 - 1`。例：`[[9,9,4],[6,6,8],[2,1,1]]` → `4`（路径 `1 -> 2 -> 6 -> 9`）；`[[3,4,5],[3,2,6],[2,2,1]]` → `4`（路径 `3 -> 4 -> 5 -> 6`）；`[[1]]` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 「相邻且更大」把格子连成一张有向无环图（DAG），最长递增路径就是这张图的最长路径。用拓扑排序（Kahn 算法）逐层剥掉出度为 `0` 的格子（比所有邻居都大的格子），剥了几层，最长路径就有几个格子。`O(mn)`。

**识别。** 「网格 + 严格递增」→ 沿着递增边走永远不会回到原处，所以图是 DAG，不需要 `visited`；DAG 上求最长路径有两种经典做法：记忆化 DFS，或者拓扑排序按层推进。`m, n <= 200` 意味着最多 `40000` 个格子，而一条路径可以长达两万格：Python 的递归深度默认约 `1000`，记忆化 DFS 会 `RecursionError`，所以主解用拓扑排序（迭代）。

**推导。** 暴力：从每个格子出发 DFS，枚举所有递增路径，路径数指数级。浪费：从不同起点出发会重复走同一段后缀，以格子 `(i, j)` 为起点的最长路径长度其实只有一个值。洞察：把每个格子的答案缓存，就是记忆化 DFS，状态 `mn` 个，每个常数转移；换个角度，DAG 的最长路径长度等于「按拓扑层数剥洋葱」的层数：最外面一层是出度为 `0` 的格子（没有更大的邻居），剥掉它们之后，新的出度为 `0` 的格子是下一层，层数就是最长路径的格子数。

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

运行：`[[9,9,4],[6,6,8],[2,1,1]]` → `4`，`[[3,4,5],[3,2,6],[2,2,1]]` → `4`，`[[1]]` → `1`，`[[5,5],[5,5]]` → `1`；`200 x 200` 的蛇形严格递增矩阵 → `40000`，约 `15 ms`；`200 x 200` 的随机矩阵 → `13`；一条长 `20100` 格的梳状路径 → `20100`，约 `13 ms`。

**复杂度。** 时间 `O(mn)`：每个格子算一次出度、被剥一次，每次看 `4` 个邻居；空间 `O(mn)`：出度表和当前层。

**易错点。**
- 把严格大于写成大于等于：相等的邻居也算边，`[[1,1]]` 里两个格子互为出边，没有出度为 `0` 的格子，返回 `0`，正确是 `1`；`[[5,5],[5,5]]` 同样得到 `0`，正确是 `1`。
- 对角线也算邻居：示例 2 会得到比 `4` 更长的路径。
- 用递归的记忆化 DFS 直接提交：梳状矩阵（路径 `20100` 格）抛 `RecursionError`；要么改迭代，要么 `sys.setrecursionlimit` 加大线程栈。

**追问。**
- 要输出这条路径：拓扑排序时记录每个格子来自哪个邻居（`prev`），或者用记忆化 DFS 记录最优的下一格，最后沿着走。
- 先排序再 DP：把所有格子按值从小到大排序，依次更新 `length[i][j] = 1 + max(比它小的邻居的 length)`，`O(mn log mn)`，逻辑最直观，不涉及递归和出度。
- 允许相等的值（非严格递增）：不再是 DAG（相等格子可以来回走），要先把相等的连通块缩成点，复杂度和写法都变了。

**同模式。** LC 210 课程表 II、LC 207 课程表、LC 1857 有向图中最大颜色值、LC 300 最长递增子序列、LC 2050 并行课程 III。

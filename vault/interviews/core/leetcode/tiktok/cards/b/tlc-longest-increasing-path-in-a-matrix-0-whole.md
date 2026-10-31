---
id: tlc-longest-increasing-path-in-a-matrix-0-whole
node: b.longest-increasing-path-in-a-matrix
type: qa
---
## Q
**LC 329 矩阵中的最长递增路径**｜Hard · LC TikTok 全时段热度 62/100 · CodeTop 国内累计 29 次 · 最近 2026-04-23（国内 CodeTop）

给一个 `m x n` 的整数矩阵 `matrix`，求其中**最长递增路径**的长度（路径上的格子数）。每一步可以向上、下、左、右移动一格，不能走对角线，不能走出边界，路径上的值必须严格递增。`m == matrix.length`，`n == matrix[i].length`，`1 <= m, n <= 200`，`0 <= matrix[i][j] <= 2^31 - 1`。例：`[[9,9,4],[6,6,8],[2,1,1]]` → `4`（路径 `1 -> 2 -> 6 -> 9`）；`[[3,4,5],[3,2,6],[2,2,1]]` → `4`（路径 `3 -> 4 -> 5 -> 6`）；`[[1]]` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 「相邻且更大」把格子连成一张有向无环图（DAG），最长递增路径就是这张图的最长路径。记忆化 DFS：`dfs(i, j)` 是从 `(i, j)` 出发的最长递增路径点数，等于 `1 + max(严格更大的邻居的 dfs)`，每格算一次存进 `memo`，对所有格子取最大值。`O(mn)`。

**识别。** 「网格 + 严格递增」→ 沿着递增边走永远不会回到原处，所以图是 DAG，不需要 `visited`；DAG 上求最长路径最直观的做法是记忆化 DFS（另一条路是拓扑排序按层推进，见追问）。`m, n <= 200` 意味着最多 `40000` 个格子，状态 `mn` 个、每个常数次转移，足够；但递归深度可以等于路径长度，最长可达两万格，见易错点。

**推导。** 暴力：从每个格子出发 DFS，枚举所有递增路径，路径数指数级。浪费：从不同起点出发会重复走同一段后缀，以格子 `(i, j)` 为起点的最长路径长度其实只有一个值（`6 x 6` 的行优先递增矩阵不缓存要调用 `dfs` `3382` 次，却只有 `36` 个不同的格子）。洞察：把每个格子的答案缓存下来，就是记忆化 DFS：状态 `mn` 个，每个只算一次。

```python
def longest_increasing_path(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    memo = [[0] * n for _ in range(m)]         # memo[i][j]：从 (i, j) 出发的最长递增路径点数，0 表示还没算

    def dfs(i: int, j: int) -> int:
        if memo[i][j]:
            return memo[i][j]
        best = 1                               # 至少有自己
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < m and 0 <= y < n and matrix[x][y] > matrix[i][j]:
                best = max(best, 1 + dfs(x, y))   # 邻居严格更大才能走，所以不会走回头路
        memo[i][j] = best
        return best

    return max(dfs(i, j) for i in range(m) for j in range(n))
```

运行：`[[9,9,4],[6,6,8],[2,1,1]]` → `4`，`[[3,4,5],[3,2,6],[2,2,1]]` → `4`，`[[1]]` → `1`，`[[5,5],[5,5]]` → `1`；`200 x 200` 的随机矩阵 → `12`；`200 x 200` 的蛇形严格递增矩阵 → `40000`；`200 x 200` 的梳状矩阵（最长路径 `20101` 格）在默认递归上限下抛 `RecursionError`，`sys.setrecursionlimit(100000)` 后 → `20101`。

**复杂度。** 时间 `O(mn)`：每个格子的 `dfs` 只真正计算一次，每次看 `4` 个邻居；空间 `O(mn)`：`memo` 表，外加递归栈，最深等于最长路径的格子数。

**易错点。**
- 把严格大于写成大于等于：相等的邻居也算边，图里出现环，`dfs` 互相调用到 `RecursionError`；`[[1,1]]` 和 `[[5,5],[5,5]]` 都会抛错，正确答案都是 `1`。
- 对角线也算邻居：示例 2 得到 `6`，正确是 `4`。
- 递归深度：最长路径可达两万格，CPython 默认递归上限约 `1000`，会抛 `RecursionError`；`sys.setrecursionlimit(100000)` 后手写 `memo` 的版本可以跑通（梳状矩阵 → `20101`）。注意 `@cache` 的包装器是 C 实现，3.12 以后即使调高了递归上限，深递归仍会在 C 栈上限处抛 `RecursionError`（同一个梳状矩阵实测如此），所以深递归里用手写 `memo`，或者改成拓扑排序。

**追问。**
- 递归太深、不想调递归上限：拓扑排序（Kahn 算法）逐层剥掉出度为 `0` 的格子（比所有邻居都大的格子），剥了几层，最长路径就有几个格子，全程迭代，`O(mn)`：
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
- 要输出这条路径：记忆化时记录每个格子最优的下一格，最后从最大的格子沿着走；拓扑排序则记录每个格子来自哪个邻居。
- 先排序再 DP：把所有格子按值从小到大排序，依次更新 `length[i][j] = 1 + max(比它小的邻居的 length)`，`O(mn log mn)`，不涉及递归和出度。
- 允许相等的值（非严格递增）：不再是 DAG（相等格子可以来回走），要先把相等的连通块缩成点，复杂度和写法都变了。

**同模式。** LC 210 课程表 II、LC 207 课程表、LC 1857 有向图中最大颜色值、LC 300 最长递增子序列、LC 2050 并行课程 III。

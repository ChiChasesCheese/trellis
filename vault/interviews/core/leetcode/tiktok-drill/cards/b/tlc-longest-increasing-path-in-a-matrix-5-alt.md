---
id: tlc-longest-increasing-path-in-a-matrix-5-alt
node: b.longest-increasing-path-in-a-matrix
type: qa
step: 5
---
## Q
**LC 329 矩阵中的最长递增路径**｜另一种解法

记忆化 DFS 怎么写？它在 `m, n` 到 `200` 的约束下有什么坑，什么时候选它、什么时候选拓扑排序？

## A
**思路。** `dfs(i, j)` 表示从 `(i, j)` 出发的最长递增路径格子数，等于 `1 + max(dfs(邻居))`，邻居必须严格更大；用 `@cache` 缓存，对所有格子取最大值。

```python
from functools import cache


def longest_increasing_path_memo(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])

    @cache
    def dfs(i: int, j: int) -> int:        # 从 (i, j) 出发的最长递增路径点数
        best = 1
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < m and 0 <= y < n and matrix[x][y] > matrix[i][j]:
                best = max(best, 1 + dfs(x, y))
        return best

    return max(dfs(i, j) for i in range(m) for j in range(n))
```

在小矩阵上与拓扑排序版结果一致：示例 1 → `4`，示例 2 → `4`，`[[1]]` → `1`。

**坑：递归深度。** `200 x 200` 的梳状矩阵（路径有 `20100` 个格子）会触发 `RecursionError`；用 `sys.setrecursionlimit` 调大之后还要放进大栈线程（`threading.stack_size`）才能跑通，得到 `20100`。`200 x 200` 的蛇形严格递增矩阵在这个遍历顺序下没有报错，这取决于数据排布，不能据此认为递归版是安全的。

**取舍。**
- 记忆化 DFS：代码最短，状态定义最贴近题意，约束小（路径不长）时首选。
- 拓扑排序：全程迭代，不受递归深度限制，在 `m, n` 到 `200` 的约束下更稳；多一次算出度的预处理。
- 面试里可以先写记忆化 DFS，并主动指出「路径可能长达两万格，Python 默认递归深度不够」，再换成拓扑排序或排序 DP。

---
id: tlc-tt-longest-zigzag-grid-path-5-alt
node: a.tt-longest-zigzag-grid-path
type: qa
step: 5
---
## Q
**网格中最长的之字形递增路径**｜另一种解法

最长之字形递增路径（严格递增、水平竖直交替）除了「按值从大到小排序填表」，还能怎么写？写出记忆化 DFS 版本，并说明在 `m, n <= 200` 时它有什么风险、什么时候选它。

## A
**记忆化 DFS（memoized DFS）。** 直接把状态转移写成递归函数 `f(i, j, d)`，用 `@cache` 记住每个状态的结果，不需要考虑计算顺序：递增保证递归不会成环。

```python
from functools import cache

H, V = 0, 1
STEPS = (((0, 1), (0, -1)), ((1, 0), (-1, 0)))


def longest_zigzag_memo(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])

    @cache
    def f(i: int, j: int, d: int) -> int:               # 从 (i, j) 出发、下一步走方向 d
        best = 1
        for di, dj in STEPS[d]:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] > grid[i][j]:
                best = max(best, 1 + f(ni, nj, 1 - d))
        return best

    return max(f(i, j, d) for i in range(m) for j in range(n) for d in (H, V))
```

运行：`[[1,2],[4,3]]` → `4`；`[[1,2,3]]` → `2`；`[[4,2,1],[1,6,1]]` → `3`。

**风险。** 递归深度等于路径长度。交替路径可以弯来绕去覆盖大部分格子（`6 x 6` 网格里就有 32 格长的之字形路径），`200 x 200` 时远超 Python 默认的递归上限 1000，会抛 `RecursionError`。

**怎么选。**
- 面试里先写记忆化版本最快：转移和定义一一对应，不易错；写完主动指出深度问题。
- 规模大时换成排序填表（主解法），或拓扑排序（Kahn）：把每个格子的「更小邻居数」当入度，从局部最小格子出发按层推进，同样是 `O(mn)` 的状态和无递归。排序版代码最短，多一个 `log`；Kahn 版严格 `O(mn)`。

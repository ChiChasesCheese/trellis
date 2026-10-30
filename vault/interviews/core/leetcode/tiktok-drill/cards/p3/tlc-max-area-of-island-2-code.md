---
id: tlc-max-area-of-island-2-code
node: p3.max-area-of-island
type: qa
step: 2
---
## Q
**LC 695 岛屿的最大面积**｜写出 Python 实现

`m x n` 的 `0/1` 矩阵 `grid`（`1 <= m, n <= 50`），岛屿是上下左右相邻的 `1` 构成的块，面积是 `1` 的个数。返回最大岛屿面积，没有岛屿返回 `0`。

## A
**思路。** 双层循环对每个格子调用 `dfs`：`dfs(i, j)` 出界、是水或已沉过就返回 `0`；否则先把自己改成 `0`，再返回 `1` 加上四个方向的结果。所有起点的最大值就是答案。

```python
from itertools import product


def max_area_of_island(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])

    def dfs(i: int, j: int) -> int:        # 以 (i, j) 为起点沉掉整座岛，返回岛的面积
        if not (0 <= i < m and 0 <= j < n) or grid[i][j] != 1:
            return 0                       # 出界、是水、或已经沉过
        grid[i][j] = 0                     # 先沉岛再往邻居走：每格只数一次，也不会来回死循环
        return 1 + dfs(i + 1, j) + dfs(i - 1, j) + dfs(i, j + 1) + dfs(i, j - 1)

    return max(dfs(i, j) for i, j in product(range(m), range(n)))
```

运行：题面里 `8 x 13` 的示例 → `6`；`[[0,0,0,0,0,0,0,0]]` → `0`；`[[1]]` → `1`；`[[1,1],[1,1]]` → `4`；`50 x 50` 全是 `1` → `2500`（调高递归上限后）。

**复杂度。** 时间 `O(mn)`：每格至多沉岛一次，每次检查 `4` 个邻居；空间 `O(mn)`：递归栈深度最坏等于整座岛的格数。

**写法要点。** `itertools.product(range(m), range(n))` 把双层循环压成一层；`dfs` 返回面积，用 `1 + dfs(...) + ...` 一个表达式累加，不需要 `nonlocal` 计数器；`0 <= i < m` 的链式比较一行完成边界判断，和「是不是 `1`」放在同一个守卫里，水、出界、已沉都返回 `0`；原地改 `grid` 省掉 `visited`，代价是改了输入。深度：蛇形岛（`1275` 格）或 `50 x 50` 全陆地会超过 CPython 默认递归上限（约 `1000`），抛 `RecursionError`，显式栈写法见追问卡。

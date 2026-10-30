---
id: tlc-max-area-of-island-2-code
node: p3.max-area-of-island
type: qa
step: 2
---
## Q
**LC 695 岛屿的最大面积**｜写出 Python 实现

`m x n` 的 `0/1` 矩阵 `grid`（`1 <= m, n <= 50`），岛屿是上下左右相邻的 `1` 构成的块，面积是 `1` 的个数。返回最大岛屿面积，没有岛屿返回 `0`。蛇形岛屿可以很长，写法要避免递归溢出。

## A
**思路。** 双层循环找到没处理过的 `1`，用显式栈做 DFS，把搜到的每个格子立刻改成 `0` 并累计面积，取所有岛的最大值。

```python
from itertools import product


def max_area_of_island(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    best = 0
    for si, sj in product(range(m), range(n)):
        if grid[si][sj] != 1:
            continue
        grid[si][sj] = 0               # 入栈时就沉岛，保证每格只入栈一次
        stack = [(si, sj)]
        area = 0
        while stack:                   # 显式栈：岛屿可长达 2500 格，递归会爆栈
            i, j = stack.pop()
            area += 1
            for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                    grid[ni][nj] = 0
                    stack.append((ni, nj))
        best = max(best, area)
    return best
```

运行：题面里 `8 x 13` 的示例 → `6`；`[[0,0,0,0,0,0,0,0]]` → `0`；`[[1]]` → `1`；`50 x 50` 全是 `1` → `2500`；一条长 `1275` 格的蛇形岛 → `1275`。

**复杂度。** 时间 `O(mn)`：每格入栈、出栈各至多一次，每次检查 `4` 个邻居；空间 `O(mn)`：最坏情况栈里装着整座岛。

**写法要点。** `itertools.product(range(m), range(n))` 把双层循环压成一层，`continue` 提前跳过水和已处理的格子。邻居写成一个元组的元组，比 `dirs` 加下标偏移少一层间接。「入栈即标记」让每格只入栈一次，栈长度上界就是岛的大小。原地修改 `grid` 省掉 `visited`，代价是改了输入。

---
id: tlc-making-a-large-island-2-code
node: a.making-a-large-island
type: qa
step: 2
---
## Q
**LC 827 最大人工岛**｜写出 Python 实现

`n x n` 的 0/1 矩阵 `grid`（`1 <= n <= 500`），最多可把一个 `0` 改成 `1`，返回此后最大岛屿（四连通的 `1`）的面积。

## A
**思路。** 第一遍：用显式栈 DFS 给每座岛编号（`label`，从 `1` 开始）并记录面积 `size`。第二遍：枚举每个 `0`，把四邻居里**不同**的岛编号对应的面积求和再加 `1`；答案初值是原有最大岛。

```python
from collections.abc import Iterator

def largest_island(grid: list[list[int]]) -> int:
    n = len(grid)
    label = [[0] * n for _ in range(n)]            # 0 = 水或还没编号；岛从 1 开始编号
    size: dict[int, int] = {}                      # 岛编号 -> 面积

    def neighbors(i: int, j: int) -> Iterator[tuple[int, int]]:
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < n and 0 <= b < n:
                yield a, b

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and label[i][j] == 0:
                tag = len(size) + 1
                label[i][j] = tag
                stack, area = [(i, j)], 0          # 显式栈：n = 500 时递归会爆
                while stack:
                    x, y = stack.pop()
                    area += 1
                    for a, b in neighbors(x, y):
                        if grid[a][b] == 1 and label[a][b] == 0:
                            label[a][b] = tag
                            stack.append((a, b))
                size[tag] = area
    best = max(size.values(), default=0)           # 一格都不翻（或没有 0 可翻）
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                tags = {label[a][b] for a, b in neighbors(i, j)}   # 集合去重：同一座岛可能从几个方向碰到
                best = max(best, 1 + sum(size.get(t, 0) for t in tags))   # 水的编号是 0，不在 size 里，记 0
    return best
```

运行：`[[1,0],[0,1]]` → `3`，`[[1,1],[1,0]]` → `4`，`[[1,1],[1,1]]` → `4`，`[[0]]` → `1`，`[[1]]` → `1`，`[[0,0],[0,0]]` → `1`；`500×500` 全 `1`、中间一个 `0` → `250000`；`500×500` 棋盘格 → `5`。

**复杂度。** 时间 `O(n^2)`：两次遍历，每格常数次邻居检查；空间 `O(n^2)`：`label` 矩阵与最坏的栈。

**写法要点。** `neighbors` 是生成器，把四方向与边界检查封装起来，两处遍历共用；`len(size) + 1` 当作新编号，不用额外计数器；`{label[a][b] for ...}` 集合推导一步去重；水格编号是 `0`，`size.get(t, 0)` 让它自然贡献 `0`，省掉 `if t`；`max(..., default=0)` 处理没有任何岛的网格。

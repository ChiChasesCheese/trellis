---
id: tlc-number-of-distinct-islands-ii-2-code
node: a.number-of-distinct-islands-ii
type: qa
step: 2
---
## Q
**LC 711 不同岛屿的数量 II**｜写出 Python 实现

`m x n` 的二进制网格（`1 <= m, n <= 50`），四连通的 `1` 构成岛屿；形状相同或经过旋转、翻转后相同的岛屿算同一种，返回不同形状的岛屿数量。

## A
**思路。** 迭代 DFS 收集每个岛的坐标列表。`canonical` 对它做 8 种变换，每种变换后排序并平移到原点，返回 8 个形态里字典序最小的元组。所有岛的代表放进 `set`。

```python
from itertools import product


def canonical(cells: list[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    forms = []
    for sx, sy, swap in product((1, -1), (1, -1), (False, True)):   # 4 种符号 x 是否交换 = 8 种旋转/翻转
        pts = sorted((sx * (y if swap else x), sy * (x if swap else y)) for x, y in cells)
        ox, oy = pts[0]                                            # 排序后第一个点平移到原点
        forms.append(tuple((x - ox, y - oy) for x, y in pts))
    return min(forms)                                              # 8 个形态里字典序最小的当代表


def num_distinct_islands2(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    seen = [[False] * n for _ in range(m)]
    shapes: set[tuple[tuple[int, int], ...]] = set()
    for i in range(m):
        for j in range(n):
            if grid[i][j] and not seen[i][j]:
                cells: list[tuple[int, int]] = []
                seen[i][j] = True
                stack = [(i, j)]
                while stack:                                       # 迭代 DFS，岛最大 2500 格，不递归
                    x, y = stack.pop()
                    cells.append((x, y))
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] and not seen[nx][ny]:
                            seen[nx][ny] = True
                            stack.append((nx, ny))
                shapes.add(canonical(cells))
    return len(shapes)
```

运行：`[[1,1,0,0,0],[1,0,0,0,0],[0,0,0,0,1],[0,0,0,1,1]]` → `1`；`[[1,1,0,0,0],[1,1,0,0,0],[0,0,0,1,1],[0,0,0,1,1]]` → `1`；`[[0]]` → `0`；`[[1]]` → `1`；`L` 形与镜像的 `J` 形并排 → `1`；`50 x 50` 全 `1` → `1`。

**复杂度。** 时间 `O(mn log(mn))`：每格访问一次，每个岛做 8 次排序；空间 `O(mn)`：`seen`、栈和集合。

**写法要点。** `itertools.product` 一次枚举出 `(sx, sy, swap)` 的 8 种组合，替代手写 8 个 `lambda`；排序后的元组天然可哈希、可比较，`min(forms)` 直接按字典序取最小；用显式栈代替递归，避开 `2500` 格大岛的递归深度问题。

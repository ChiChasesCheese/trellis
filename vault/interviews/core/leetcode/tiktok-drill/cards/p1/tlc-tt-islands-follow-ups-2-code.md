---
id: tlc-tt-islands-follow-ups-2-code
node: p1.tt-islands-follow-ups
type: qa
step: 2
---
## Q
**岛屿数量及其追问集合**｜写出 Python 实现

`grid` 是 `m x n` 的 0/1 网格，`1 <= m, n <= 300`，四方向相连的 `1` 构成一座岛。写 `num_islands(grid)`（不修改网格）、`num_distinct_islands(grid)`（只允许平移时形状不同的岛屿数）、`num_distinct_islands_ii(grid)`（允许旋转、翻转）。

## A
**思路。** 一个生成器 `components` 用显式栈逐座产出岛屿的格子坐标，`seen` 另存；三个函数都建立在它之上。形状签名是平移到以最小格为原点后排序的坐标元组；允许旋转翻转时对 8 种变换各算一个，取字典序最小的。

```python
from collections.abc import Iterator

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def components(grid: list[list[int]]) -> Iterator[list[tuple[int, int]]]:
    """逐个产出岛屿的格子列表；不修改 grid，visited 单独记。"""
    m, n = len(grid), len(grid[0])
    seen = [[False] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            if grid[r][c] != 1 or seen[r][c]:
                continue
            seen[r][c] = True
            cells, stack = [], [(r, c)]
            while stack:                                    # 显式栈，不受递归深度限制
                x, y = stack.pop()
                cells.append((x, y))
                for dx, dy in DIRS:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1 and not seen[nx][ny]:
                        seen[nx][ny] = True                 # 入栈时就标记，避免重复入栈
                        stack.append((nx, ny))
            yield cells


def num_islands(grid: list[list[int]]) -> int:
    return sum(1 for _ in components(grid))


def num_distinct_islands(grid: list[list[int]]) -> int:
    """形状相同（只允许平移）算同一种：格子坐标减去最小的 (行, 列) 后排序，作为形状签名。"""
    shapes = set()
    for cells in components(grid):
        r0, c0 = min(cells)                                 # 行优先最小的格子当原点
        shapes.add(tuple(sorted((r - r0, c - c0) for r, c in cells)))
    return len(shapes)


# 8 种变换 = 4 次旋转 × 是否翻转，即 (x, y) 的全部「换序加变号」
TRANSFORMS = (lambda x, y: (x, y), lambda x, y: (x, -y), lambda x, y: (-x, y), lambda x, y: (-x, -y),
              lambda x, y: (y, x), lambda x, y: (y, -x), lambda x, y: (-y, x), lambda x, y: (-y, -x))


def num_distinct_islands_ii(grid: list[list[int]]) -> int:
    """旋转、翻转后相同也算同一种：8 种变换各自归一化，取字典序最小的作为签名。"""
    shapes = set()
    for cells in components(grid):
        forms = []
        for f in TRANSFORMS:
            pts = [f(x, y) for x, y in cells]
            x0, y0 = min(pts)
            forms.append(tuple(sorted((x - x0, y - y0) for x, y in pts)))
        shapes.add(min(forms))
    return len(shapes)
```

运行：`[[1,1,0,0,0],[1,1,0,0,0],[0,0,1,0,0],[0,0,0,1,1]]` → `num_islands` 为 `3`，调用后网格不变；`[[1,1,0,1,1],[1,0,0,0,0],[0,0,0,0,1],[1,1,0,1,1]]` → `4`、`3`、`2`；`[[1,1,0,0,0],[1,0,0,0,0],[0,0,0,0,1],[0,0,0,1,1]]` → 平移意义下 `2` 种，允许旋转翻转 `1` 种；`[[0]]` → `0`，`[[1]]` → `1`；`300 x 300` 全 `1` 与蛇形岛屿 → `1`。

**复杂度。** `num_islands` 时间 `O(mn)`、空间 `O(mn)`；形状版本每座岛多一次排序，总计 `O(mn log mn)`，旋转翻转版常数乘 8。

**写法要点。**
- 生成器 `yield cells`：计数、去重、求面积都复用同一段搜索，调用方想怎么消费就怎么消费。
- `seen` 用 `[[False] * n for _ in range(m)]`，每行独立；`[[False] * n] * m` 的各行是同一个对象。
- `min(cells)` 对元组按字典序取最小，正好得到「行优先最小的格子」，不需要手写比较。
- 形状签名是 `tuple`：可哈希，能直接放进 `set`；用 `list` 会 `TypeError: unhashable type`。

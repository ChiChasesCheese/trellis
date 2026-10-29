---
id: tlc-tt-islands-follow-ups-0-whole
node: a.tt-islands-follow-ups
type: qa
---
## Q
**岛屿数量及其追问集合**｜Hard · 近一年被问：美国 14 次、国内 10 次 · 最近 2026-10（面试记录）

给一个 `m x n` 的二维 0/1 网格 `grid`，`1 <= m, n <= 300`，`1` 是陆地、`0` 是水，上下左右相连的陆地构成一座岛屿。依次回答：（1）岛屿数量，**不能修改**原网格；（2）形状不同的岛屿数量（只允许平移）；（3）旋转、翻转后相同也算同一种形状。例：`grid = [[1,1,0,1,1],[1,0,0,0,0],[0,0,0,0,1],[1,1,0,1,1]]` → 岛屿数 `4`，平移意义下不同的形状 `3` 种，允许旋转翻转时 `2` 种。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用显式栈做 DFS，访问标记单独存放（不改网格），一个生成器逐座产出岛屿的格子坐标：岛屿数就是产出的座数；形状签名是「格子坐标减去最小坐标后排序成元组」，平移不变；允许旋转翻转时，对 8 种变换各算一个签名，取最小的那个。

**识别。** 「统计连通块」是 flood fill（洪水填充）或并查集；`300 x 300` 是 `9 * 10^4` 格，`O(mn)` 即可。递归 DFS 在蛇形岛屿上深度可达 `9 * 10^4`，Python 默认递归上限 `1000`，所以用显式栈。「不修改原网格」意味着访问标记另开 `seen`。「形状相同」要一个平移不变的规范形（canonical form）当哈希键；「旋转翻转也相同」就对 8 种变换（4 次旋转乘是否翻转）各取规范形再取最小。

**推导。** 暴力：对每个陆地格都做一次完整搜索再去重，`O((mn)^2)`。浪费：同一座岛被它的每个格子重复搜索。洞察：搜到就标记 `seen`，每格只进栈一次，`O(mn)`。形状：两两比较岛屿太慢，改成「规范形做哈希键」，每座岛排序一次，总计 `O(mn log mn)`；规范形是把坐标整体平移到以最小格为原点，旋转翻转则在 8 种变换里取字典序最小的规范形。

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

运行：`[[1,1,0,0,0],[1,1,0,0,0],[0,0,1,0,0],[0,0,0,1,1]]` → `num_islands` 为 `3`，调用后网格不变；开头的例子 → `4`、`3`、`2`；`[[1,1,0,0,0],[1,0,0,0,0],[0,0,0,0,1],[0,0,0,1,1]]`（两个 L 形，朝向不同）→ 平移意义下 `2` 种，允许旋转翻转 `1` 种；`[[0]]` → `0`，`[[1]]` → `1`；`300 x 300` 全 `1` 与蛇形岛屿 → `1`，不会 `RecursionError`。

**复杂度。** `num_islands` 为 `O(mn)` 时间、`O(mn)` 空间（`seen` 和栈）；形状版本每座岛多一次排序，总计 `O(mn log mn)`，旋转翻转版常数乘 8。

**易错点。**
- 递归 DFS：`300 x 300` 全 `1` 的网格会直接 `RecursionError`（默认上限 `1000`）。
- 形状签名没有平移归一化：用绝对坐标当签名，开头的例子得到 `4`，正确是 `3`。
- 少了翻转、只做 4 种旋转：`["011","110","000","110","011"]`（一个 S 形、一个 Z 形）得到 `2` 种，正确是 `1` 种。
- 访问数组写成 `[[False] * n] * m`：所有行是同一个列表，标记一格等于标记整列，开头的例子得到 `2`，正确是 `4`。

**追问。**
- 地图太大放不进内存：分块处理，块内用并查集，再把块边界上相邻的两格陆地所属的集合合并，数最后的根。
- 流式输入：逐行读，只保存上一行每格的并查集标签，内存 `O(n)`。
- 其他变体：8 方向（`DIRS` 加 4 个对角）、最大面积（LC 695，取 `max(len(cells))`）、最大人工岛（LC 827）。

**同模式。** LC 200 岛屿数量、LC 694 不同岛屿的数量、LC 711 不同岛屿的数量 II、LC 695 岛屿的最大面积、LC 827 最大人工岛、LC 130 被围绕的区域。

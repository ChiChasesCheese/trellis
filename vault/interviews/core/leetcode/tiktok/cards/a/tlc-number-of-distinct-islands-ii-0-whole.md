---
id: tlc-number-of-distinct-islands-ii-0-whole
node: a.number-of-distinct-islands-ii
type: qa
---
## Q
**LC 711 不同岛屿的数量 II**｜Hard · 近一年被问：美国 14 次、国内 10 次 · 最近 2026-10（面试记录）

给 `m x n` 的二进制网格 `grid`，岛屿是由四连通（上下左右）的 `1` 组成的块，网格四周视为海水。两个岛屿如果**形状相同**，或者经过**旋转**（顺时针 `90°`、`180°`、`270°`）、**翻转**（左右、上下）后形状相同，就算同一种。返回网格里**不同形状**的岛屿数量。`1 <= m, n <= 50`，`grid[i][j]` 是 `0` 或 `1`。例：`[[1,1,0,0,0],[1,0,0,0,0],[0,0,0,0,1],[0,0,0,1,1]]` → `1`（两个岛屿互为 `180°` 旋转）；`[[1,1,0,0,0],[1,1,0,0,0],[0,0,0,1,1],[0,0,0,1,1]]` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用 DFS 收集每个岛屿的格子，对格子做 8 种旋转 / 翻转变换，每种变换后排序并把最小的点平移到原点，取字典序最小的形态当「规范形」（canonical form），放进集合去重；答案是集合大小。

**识别。** 「形状相同（含旋转、翻转）」= 给每个对象找一个**规范代表**，再哈希去重。只允许平移的版本是 LC 694；加上旋转、翻转后，每个形状有 8 种摆法（正方形的对称群，8 个元素）。网格最大 `50 x 50`，一个岛最多 `2500` 格，每格做 8 次变换完全来得及。

**推导。** 暴力：岛屿两两比较，每对检查 8 种变换是否重合，`O(k^2)` 对 × 每对的排序与比较 → 「相同」是等价关系，没必要两两比，给每个等价类选一个唯一代表即可 → 平移归一：排序后把第一个点挪到 `(0, 0)`；旋转 / 翻转：`(x, y)` 变成 `(±x, ±y)` 或 `(±y, ±x)`，共 8 种 → 同一类的岛屿，8 个形态的集合完全相同，取其中字典序最小的就是同一个代表 → 每个岛屿 `O(8 s log s)`。

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

运行：两个示例都是 `1`；`[[0]]` → `0`；`[[1]]` → `1`；`[[1,0,0,0,1],[1,0,0,0,1],[1,1,0,1,1]]`（一个 `L` 形和它的镜像 `J` 形）→ `1`；`50 x 50` 全是 `1`（一个 `2500` 格的岛）→ `1`，毫秒级。

**复杂度。** 时间 `O(mn log(mn))`：每格进入某个岛一次，每个岛做 8 次 `O(s log s)` 的排序；空间 `O(mn)`。

**易错点。**
- 只处理 4 种旋转、漏掉翻转：上面的 `L` / `J` 例子会数成 `2`，正确是 `1`。
- 变换后不平移归一化：直接比较绝对坐标，示例 1 的两个岛（位置不同）被数成 `2`，正确是 `1`。
- 用格子数当「指纹」：`I` 形四格（一条线）和 `L` 形四格形状不同，却会被数成同一种，`[[1,1,1,1,0,1,0],[0,0,0,0,0,1,0],[0,0,0,0,0,1,1]]` 得到 `1`，正确是 `2`。

**追问。**
- 只允许平移（LC 694）：去掉其余 7 种变换，只做排序加平移，或者用 DFS 的方向序列当签名。
- 要统计每种形状有几个岛：把 `shapes` 换成 `Counter`，对每个 `canonical(cells)` 计数。
- 另一种去重写法：把一个岛的 8 个形态都放进「已见」集合，见到新岛时只查它的第一个形态是否已在集合里；这样不需要取最小值，每类多占 8 倍空间。

**同模式。** LC 694 不同岛屿的数量、LC 695 岛屿的最大面积、LC 200 岛屿数量、LC 827 最大人工岛、LC 1905 统计子岛屿。

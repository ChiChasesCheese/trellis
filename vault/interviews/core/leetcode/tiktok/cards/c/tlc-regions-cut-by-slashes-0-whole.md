---
id: tlc-regions-cut-by-slashes-0-whole
node: c.regions-cut-by-slashes
type: qa
---
## Q
**LC 959 由斜杠划分区域**｜Medium · LC TikTok 全时段热度 41/100

一个 `n x n` 的网格，每个 `1 x 1` 的方块里是 `'/'`、`'\'` 或空格，字符会把方块划分成若干共边的区域。`grid` 是字符串数组，返回区域的数量。反斜杠要转义，`'\'` 在输入里写成 `'\\'`。`n == grid.length == grid[i].length`，`1 <= n <= 30`，`grid[i][j]` 是 `'/'`、`'\'` 或 `' '`。例：`[" /","/ "]` → `2`；`[" /","  "]` → `1`；`["/\\","\\/"]` → `5`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 每个方块按对角线拆成上、右、下、左 4 个小三角形做节点，用并查集（Union-Find）按斜杠和相邻关系合并，区域数就是集合数，`O(n² α(n²))`。

**识别。** 「线把平面切成块，数块数」就是数连通分量；难点是斜杠切开的是方块内部，所以节点要细到三角形。`n <= 30` 时只有 3600 个节点，什么方法都够。

**推导。** 方块当节点会把 `'/'` 里的两个区域并成一个。拆成 4 个三角形后：空格全连通；`'/'` 连（上、左）和（下、右）；`'\'` 连（上、右）和（下、左）；方块之间，下三角连下一行的上三角，右三角连右边方块的左三角（线不会穿过方块的边）。初始 `4n²` 个集合，每次成功合并减 1，剩下的就是答案。

```python
def regions_by_slashes(grid: list[str]) -> int:
    n = len(grid)
    parent = list(range(4 * n * n))                    # 方块 (r,c) 的 4 个三角形：0 上 1 右 2 下 3 左
    regions = 4 * n * n                                # 初始每个三角形自成一块

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]              # 路径减半，摊还接近 O(1)
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        nonlocal regions
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            regions -= 1                               # 每成功合并一次，区域少一块

    for r in range(n):
        for c in range(n):
            top = (r * n + c) * 4
            right, bottom, left = top + 1, top + 2, top + 3
            ch = grid[r][c]
            if ch == "/":                              # '/' 把方块切成左上、右下两半
                union(top, left)
                union(bottom, right)
            elif ch == "\\":                           # '\' 切成右上、左下两半
                union(top, right)
                union(bottom, left)
            else:                                      # 空格：四块全连通
                union(top, right)
                union(right, bottom)
                union(bottom, left)
            if r + 1 < n:
                union(bottom, ((r + 1) * n + c) * 4)           # 下三角 <-> 下方方块的上三角
            if c + 1 < n:
                union(right, (r * n + c + 1) * 4 + 3)          # 右三角 <-> 右边方块的左三角
    return regions
```

运行：`[" /","/ "]` → `2`，`[" /","  "]` → `1`，`["/\\","\\/"]` → `5`；`[" "]` → `1`，`["/"]` → `2`，`["\\"]` → `2`；`30 x 30` 全是 `'/'` → `60`。

**复杂度。** 时间 `O(n² α(n²))`，空间 `O(n²)`。

**拓展优化。**
- 按大小合并（union by size）配合路径压缩，`find` 严格逼近 `O(1)`；`n <= 30` 时路径减半已够用。
- 不用并查集：每个方块放大成 `3 x 3`，斜杠画成对角线上的 3 个墙格，再用 BFS 数 `3n x 3n` 矩阵里空地的连通块；缺点是对角线方向容易画反。

```python
from collections import deque


def regions_by_slashes_scale3(grid: list[str]) -> int:
    n = len(grid)
    wall = [[0] * (3 * n) for _ in range(3 * n)]
    for r in range(n):
        for c in range(n):
            for k in range(3):                         # 在 3x3 里画对角线
                if grid[r][c] == "/":
                    wall[3 * r + k][3 * c + 2 - k] = 1
                elif grid[r][c] == "\\":
                    wall[3 * r + k][3 * c + k] = 1
    regions = 0
    for sr in range(3 * n):
        for sc in range(3 * n):
            if wall[sr][sc]:
                continue
            regions += 1                               # 遇到一块没数过的空地：新区域
            wall[sr][sc] = 1                           # 入队即标记，同一格不会入队两次
            queue = deque([(sr, sc)])
            while queue:
                r, c = queue.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < 3 * n and 0 <= nc < 3 * n and not wall[nr][nc]:
                        wall[nr][nc] = 1
                        queue.append((nr, nc))
    return regions
```


**易错点。**
- 方块当单个节点：`["/"]` 算成 `1`，正确是 `2`。
- 跨方块的连接接成同名三角：必须是下三角接下方的**上**三角、右三角接右边的**左**三角。
- 比较反斜杠要写 `ch == "\\"`；写成 `"\"` 是语法错误。

**追问。**
- 每个区域的面积：把三角形按根分组计数，每个三角形占方块的 1/4。
- 斜杠不是对角线或格子不是方形：「每格固定切 4 块」的前提失效，要重新设计节点。

**同模式。** LC 200 岛屿数量、LC 547 省份数量、LC 130 被围绕的区域、LC 1020 飞地的数量、LC 765 情侣牵手。

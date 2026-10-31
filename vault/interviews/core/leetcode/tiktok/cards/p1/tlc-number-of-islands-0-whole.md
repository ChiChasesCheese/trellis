---
id: tlc-number-of-islands-0-whole
node: p1.number-of-islands
type: qa
---
## Q
**LC 200 岛屿数量**｜Medium · LC TikTok 近 30 天热度 100/100（全时段 100） · 近一年被问：美国 14 次、国内 10 次 · CodeTop 国内累计 192 次 · 最近 2026-10（美国面试记录）

给一个由 `'1'`（陆地）和 `'0'`（水）组成的二维网格 `grid`，数其中岛屿的数量。岛屿由水平或竖直方向相邻的陆地连成，四条边外面都是水。`m == grid.length`，`n == grid[i].length`，`1 <= m, n <= 300`，`grid[i][j]` 是 `'0'` 或 `'1'`。例：`[["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]` → `1`；`[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]` → `3`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 按行扫描网格，每遇到一块还没处理的陆地就计数加一，并用一次搜索（DFS 或 BFS）把整座岛"沉掉"（改成 `'0'`），这样同一座岛只会被数一次。`O(mn)`。

**识别。** 「二维网格 + 上下左右相邻 + 数连通的一块」就是数连通分量（connected components），工具是 DFS / BFS / 并查集（Union-Find）。`m, n <= 300` 意味着最多 `9 * 10^4` 格，`O(mn)` 足够，朴素的递归 DFS 就是正解。

**推导。** 暴力：对每个陆地格各做一次搜索并不记录哪些格已经搜过，同一座岛的每一格都当一次起点，岛被重复数很多次。浪费在「搜过的格子没有留下记号」。洞察：第一次碰到一座岛时顺手把它整个标成已访问，之后扫描再遇到这座岛的格子就会跳过；每格最多被标记一次，总共 `O(mn)`。

```python
def num_islands(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def sink(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return                                      # 出界或水：这条搜索到头
        grid[r][c] = "0"                                # 先沉掉再往四周搜，同一格不会被重复进入
        sink(r + 1, c)
        sink(r - 1, c)
        sink(r, c + 1)
        sink(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1                              # 找到一座新岛：把它整座沉掉
                sink(r, c)
    return count
```

运行：两个示例输出 `1` 和 `3`；`[["0"]]` → `0`，`[["1"]]` → `1`；`[["1","0","1"],["1","1","1"]]` → `1`；`300 x 300` 全是 `"1"`，默认递归上限下抛 `RecursionError`，把上限调到 200000 后输出 `1`。

**复杂度。** 时间 `O(mn)`，每格最多被沉掉一次、被检查常数次；空间最坏 `O(mn)`（递归栈，全是陆地时深度可达 `mn`）。

**拓展优化。**
- 递归深度超过约 1000 层会抛 `RecursionError`，改成显式栈：
```python
def num_islands_stack(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r0 in range(rows):
        for c0 in range(cols):
            if grid[r0][c0] != "1":
                continue
            count += 1
            grid[r0][c0] = "0"                      # 入栈时就沉掉，同一格不会入栈两次
            stack = [(r0, c0)]
            while stack:                            # 栈深不受递归限制
                r, c = stack.pop()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                        grid[nr][nc] = "0"
                        stack.append((nr, nc))
    return count
```
- 并查集（Union-Find）：不用搜索；陆地一个个加入（LC 305）时同一结构可在线更新：
```python
def num_islands_uf(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])
    parent = list(range(rows * cols))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]           # 路径折半，摊还近似 O(1)
            x = parent[x]
        return x

    count = sum(cell == "1" for row in grid for cell in row)   # 先当作每块陆地各是一座岛
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            for nr, nc in ((r + 1, c), (r, c + 1)):  # 只看右、下，每对邻居只处理一次
                if nr < rows and nc < cols and grid[nr][nc] == "1":
                    a, b = find(r * cols + c), find(nr * cols + nc)
                    if a != b:
                        parent[a] = b
                        count -= 1                  # 成功合并两个集合，岛数少一
    return count
```

**易错点。**
- 四个方向都要搜。只向右、向下搜，U 形的岛会被拆开：`[["1","0","1"],["1","1","1"]]` 会数成 `2`，正确是 `1`。
- 格子里是字符串 `"1"` 不是整数 `1`，比较写错会让结果恒为 `0`。
- 原地改 `grid` 会破坏输入；调用方还要用这张图时改用 `visited` 集合。
- 递归深度：整片陆地时一次 `sink` 可以嵌套到 `mn`（最坏 `9 * 10^4` 层），CPython 默认上限约 1000，会抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成显式栈（见拓展优化）。

**追问。**
- 岛屿最大面积（LC 695）：搜索时累计格数，取最大值。
- 陆地一个个加入、每次加完都要答岛屿数（LC 305）：用拓展优化里的并查集，新增陆地先计数加一，每合并一对不同的集合就减一。
- 八个方向都算相邻：把方向元组换成八个。

**同模式。** LC 695 岛屿的最大面积、LC 130 被围绕的区域、LC 694 不同岛屿的数量、LC 305 岛屿数量 II、LC 733 图像渲染、LC 1020 飞地的数量。

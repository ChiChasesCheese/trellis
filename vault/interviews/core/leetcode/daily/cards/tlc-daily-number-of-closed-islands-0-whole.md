---
id: tlc-daily-number-of-closed-islands-0-whole
node: graph-traversal.number-of-closed-islands
type: qa
---
## Q
**LC 1254 统计封闭岛屿的数目**｜Medium

二维矩阵 `grid` 由 `0`（土地）和 `1`（水）组成。岛是由最大的 4 个方向（上下左右）连通的 `0` 组成的群；封闭岛是**完全**由 `1` 包围（左、上、右、下）的岛。返回封闭岛屿的数目。`1 <= grid.length, grid[0].length <= 100`，`0 <= grid[i][j] <= 1`。例：`grid = [[0,0,1,0,0],[0,1,0,1,0],[0,1,1,1,0]]` → `1`；`grid = [[1,1,1,1,1,1,1],[1,0,0,0,0,0,1],[1,0,1,1,1,0,1],[1,0,1,0,1,0,1],[1,0,1,1,1,0,1],[1,0,0,0,0,0,1],[1,1,1,1,1,1,1]]` → `2`（外圈一个，中间那一格一个）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 网格连通块 DFS（flood fill），连通块是否碰到边界。

**核心题。**

- LC 200 岛屿数量（Blind 75、NeetCode 150、Hot 100、Top Interview 150）：同一个 flood fill 数连通块
- LC 130 被围绕的区域（NeetCode 150、Top Interview 150）：同样判断连通块是否碰到边界

**一句话。** 对每个没访问过的土地做一次 DFS 淹掉整个岛，DFS 返回「这个岛是否从未走出网格」；返回真的岛数一个。

**识别。** 「4 连通的最大一块」是连通块，「完全被包围」等价于「这一块没有任何格子在边界上」（出界即不封闭）。`m, n <= 100`，每格只访问一次，`O(mn)` 足够。

**推导。** 先数所有岛再逐个判断边界，要么存两遍状态，要么重复遍历。把判断塞进 DFS：越界返回 `False`，遇到水返回 `True`，遇到土地先标记为水（避免重复访问和环），再把四个方向**全部**走完并汇总；这样一次遍历就同时淹掉整块岛并得到它封闭与否。

```python
def closed_island(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])

    def dfs(i: int, j: int) -> bool:
        if not (0 <= i < m and 0 <= j < n):
            return False                       # 走出网格：这个岛碰到了边界，不封闭
        if grid[i][j] == 1:
            return True                        # 水（或已访问）：这个方向被围住
        grid[i][j] = 1                         # 先淹掉，防止重复访问
        closed = True
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if not dfs(i + di, j + dj):        # 四个方向都要走完：不能短路，否则整块岛淹不完
                closed = False
        return closed

    return sum(grid[i][j] == 0 and dfs(i, j) for i in range(m) for j in range(n))
```

运行：`[[0,0,1,0,0],[0,1,0,1,0],[0,1,1,1,0]]` → `1`；`7×7` 的回字形 → `2`；`[[1,1,1,1,1,1,1,0],[1,0,0,0,0,1,1,0],[1,0,1,0,1,1,1,0],[1,0,0,0,0,1,0,1],[1,1,1,1,1,1,1,0]]` → `2`；`[[0]]` → `0`。

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`（递归栈最深为整个网格的格数）。注意 `dfs` 会修改 `grid`。

**易错点。**
- 用 `dfs(a) and dfs(b) and …` 连接四个方向：遇到第一个 `False` 就短路，这块岛剩下的格子没被淹掉，之后被当成新的岛重复判断。`[[1,1,1,1],[1,1,0,1],[1,0,0,1],[1,1,0,1]]` 得到 `1`，正确是 `0`（最后一行的 `0` 在边界上）。
- 递归深度：一条蛇形的岛能让递归深度达到数千（例如 `100 × 100` 的蛇形岛），CPython 默认上限约 `1000`，会抛 `RecursionError`；需要 `sys.setrecursionlimit` 或改成迭代。
- 先递归、后标记（或忘了标记）：相邻两格互相调用，永不终止，直接 `RecursionError`；进入格子的第一件事是把它改成 `1`。

**追问。** 迭代版：先从四条边上的每个 `0` 出发淹掉所有与边界相连的土地，再数剩下的连通块：
```python
def closed_island_iter(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])

    def flood(si: int, sj: int) -> None:
        stack = [(si, sj)]
        grid[si][sj] = 1
        while stack:
            i, j = stack.pop()
            for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= a < m and 0 <= b < n and grid[a][b] == 0:
                    grid[a][b] = 1
                    stack.append((a, b))

    for i in range(m):                         # 与边界相连的土地一律不封闭
        for j in range(n):
            if (i in (0, m - 1) or j in (0, n - 1)) and grid[i][j] == 0:
                flood(i, j)
    count = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0:                # 剩下的每个连通块都是封闭岛
                count += 1
                flood(i, j)
    return count
```
也可以用并查集：把边界外的虚拟节点与所有边界土地合并，数不与虚拟节点相连的土地连通块。

**同模式。** LC 200 岛屿数量、LC 130 被围绕的区域、LC 1020 飞地的数量、LC 695 岛屿的最大面积。

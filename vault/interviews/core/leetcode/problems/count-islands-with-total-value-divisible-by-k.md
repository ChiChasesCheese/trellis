---
slug: count-islands-with-total-value-divisible-by-k
---
## Q
**LC 3619 总价值可以被 K 整除的岛屿数目**｜Medium

给你一个 `m x n` 的矩阵 `grid` 和一个正整数 `k`。一个岛屿是由**正**整数（表示陆地）组成的，陆地间四周（水平或垂直）连通。岛屿的总价值是该岛屿中所有单元格的值之和。返回总价值可以被 `k` 整除的岛屿数量。`m == grid.length`，`n == grid[i].length`，`1 <= m, n <= 1000`，`1 <= m * n <= 10^5`，`0 <= grid[i][j] <= 10^6`，`1 <= k <= 10^6`。

例：`grid = [[0,2,1,0,0],[0,5,0,0,5],[0,0,1,0,0],[0,1,4,7,0],[0,2,0,0,8]]`，`k = 5` → `2`（四个岛屿，总价值分别为 `8`、`5`、`15`、`8`，其中 `5` 和 `15` 能被 5 整除）；`grid = [[3,0,3,0],[0,3,0,3],[3,0,3,0]]`，`k = 3` → `6`（六个单格岛屿，每个都是 3 的倍数）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 网格连通块（Flood Fill）+ 每个连通块累加一个值，最后对块总和取模判断。

**核心题。**

- LC 200 岛屿数量（Blind 75、NeetCode 150、Hot 100、Top Interview 150）：同一个 flood fill：这里多了每个连通块累加格子值再对 `k` 取模

**一句话。** 扫描网格，遇到没访问过的陆地就从它出发做一次 DFS，沿途把格子值累加并把格子清零（标记已访问），DFS 返回时得到整座岛屿的总价值，总价值 `% k == 0` 就计一座。

**识别。** 「四周连通的正整数」就是求连通块；要的是每个连通块的**和**而不是面积，所以 DFS 要返回一个数而不是计数；`m * n <= 10^5`，每格只访问一次的 `O(m * n)` 足够。

**推导。** 直接做：先找出所有岛屿再分别求和，需要存下每座岛屿的格子，白占内存。把求和嵌进 DFS：函数返回「从这个格子出发能连到的全部陆地的值之和」，等于本格的值加上四个邻居的返回值；访问过的格子清零，同时当成水，既防止重复统计，也省掉 `visited`。外层每遇到一个还没清零的陆地（值 `> 0`）就是一座新岛屿的入口。

```python
def count_islands(grid: list[list[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])

    def dfs(i: int, j: int) -> int:
        # 返回从 (i, j) 连出去的整座岛屿尚未统计部分的价值和
        if not (0 <= i < m and 0 <= j < n) or grid[i][j] == 0:
            return 0                        # 出界或水（包括已访问被清零的格子）
        total = grid[i][j]
        grid[i][j] = 0                      # 清零 = 标记已访问，直接改输入，省掉 visited
        return total + dfs(i + 1, j) + dfs(i - 1, j) + dfs(i, j + 1) + dfs(i, j - 1)

    # 只有入口是陆地（> 0）才开一座新岛屿；and 的短路保证水格不会进 dfs
    return sum(grid[i][j] > 0 and dfs(i, j) % k == 0
               for i in range(m) for j in range(n))
```

运行：示例 1 → `2`；示例 2 → `6`。

**拓展。** 递归深度最坏接近陆地格数；显式栈版本不受 Python 递归上限影响，其余逻辑相同：
```python
def count_islands_stack(grid: list[list[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])
    ans = 0
    for si in range(m):
        for sj in range(n):
            if grid[si][sj] == 0:
                continue
            total, stack = grid[si][sj], [(si, sj)]
            grid[si][sj] = 0                # 入栈时就清零，避免同一格被压栈两次
            while stack:
                i, j = stack.pop()
                for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                    if 0 <= a < m and 0 <= b < n and grid[a][b]:
                        total += grid[a][b]
                        grid[a][b] = 0
                        stack.append((a, b))
            ans += total % k == 0
    return ans
```

**复杂度。** 时间 `O(m * n)`：每个格子最多被 DFS 访问一次；空间 `O(m * n)`（递归栈最深，一条蛇形岛屿）。

**易错点。**
- 递归深度：一座覆盖整个网格的蛇形（或实心）岛屿，递归深度可达 `m * n = 10^5`，而 CPython 默认递归上限约 1000，`316 x 316` 的全陆地网格就会抛 `RecursionError`；要么调高 `sys.setrecursionlimit`，要么改用上面的显式栈。
- 外层把水格也送进 DFS：水格返回的总价值是 `0`，`0 % k == 0` 会把每个水格都当成一座岛屿，示例 1 会远大于 `2`。
- 把对角线也当作连通：只能四个方向。

**同模式。** LC 200 岛屿数量、LC 695 岛屿的最大面积、LC 1254 统计封闭岛屿的数目、LC 1020 飞地的数量。

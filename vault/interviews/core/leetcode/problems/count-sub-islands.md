---
slug: count-sub-islands
---
## Q
**LC 1905 统计子岛屿**｜Medium

两个 `m × n` 的 0/1 网格 `grid1` 和 `grid2`，`1` 是陆地，岛屿是四方向相连的陆地。若 `grid2` 的一座岛屿的每个陆地格子，在 `grid1` 中对应位置也是陆地，它就是子岛屿。统计 `grid2` 中子岛屿的数目。

## A
**一句话。** 对 `grid2` 的每座岛 DFS（并把走过的格子沉掉），只要岛里有一格在 `grid1` 是海，这座岛就不是子岛屿。

```python
def count_sub_islands(grid1, grid2):
    m, n = len(grid2), len(grid2[0])
    def dfs(i, j):               # 这座岛是否整体落在 grid1 的陆地上
        if not (0 <= i < m and 0 <= j < n):
            return True
        if not grid2[i][j]:
            return True
        grid2[i][j] = 0          # 沉岛，防重复访问
        ok = grid1[i][j] == 1
        for x, y in ((i + 1, j), (i - 1, j),
                     (i, j + 1), (i, j - 1)):
            ok = dfs(x, y) and ok   # 先递归，保证整座岛都被沉掉
        return ok
    return sum(grid2[i][j] == 1 and dfs(i, j)
               for i in range(m) for j in range(n))
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`（递归栈）。

**易错点。**
- 写成 `ok and dfs(x, y)`：`ok` 为假时短路，岛屿剩余部分没被沉掉，会被当成新岛屿再数一次。
- 发现不合法就提前返回：同样会留下没沉的格子。
- 判断子岛屿只看起点：岛里每一格都要检查。

**追问。**
- 并查集怎么做？：对 `grid2` 建并查集，把在 `grid1` 是海的格子所在的根标成坏，最后数好的根。
- 能不 DFS 吗？：BFS 一样，关键仍是整座岛要访问完。

**同模式。** LC 695 岛屿的最大面积、LC 200 岛屿数量、LC 694 不同岛屿的数量、LC 1020 飞地的数量

---
slug: number-of-closed-islands
---
## Q
**LC 1254 统计封闭岛屿的数目**｜Medium

`0` 是土地，`1` 是水。统计上下左右四连通、且完全被水包围（不碰到网格边界）的岛屿数量。

## A
**一句话。** 对每块没访问的土地 DFS 淹掉整座岛，DFS 返回这座岛是否从未走出网格，真则计一座。

```python
def closed_island(grid):
    m, n = len(grid), len(grid[0])

    def dfs(i, j):          # 这座岛是否封闭
        if not (0 <= i < m and 0 <= j < n):
            return False    # 走出网格
        if grid[i][j]:
            return True     # 水或已访问
        grid[i][j] = 1      # 先淹掉
        res = [dfs(i+1, j), dfs(i-1, j),
               dfs(i, j+1), dfs(i, j-1)]
        return all(res)     # 四个方向都走完，不能短路

    return sum(grid[i][j] == 0 and dfs(i, j)
               for i in range(m) for j in range(n))
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 用 `dfs(a) and dfs(b) and …` 连四个方向：遇到第一个 `False` 就短路，岛没淹完，剩下的格子被当成新岛重复判断。`[[1,1,1,1],[1,1,0,1],[1,0,0,1],[1,1,0,1]]` 得 `1`，应为 `0`。
- 先递归后标记：相邻两格互相调用，永不终止，进入格子第一件事就是改成 `1`。

**追问。**
- 蛇形岛递归爆栈？：先从四条边的 `0` 出发淹掉所有与边界相连的土地（栈或 BFS），再数剩下的连通块。
- 并查集怎么做？：边界外加虚拟节点，与所有边界土地合并，数不与它相连的土地连通块。

**同模式。** LC 200 岛屿数量、LC 130 被围绕的区域、LC 1020 飞地的数量、LC 695 岛屿的最大面积

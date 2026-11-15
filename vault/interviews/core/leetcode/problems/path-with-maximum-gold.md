---
slug: path-with-maximum-gold
---
## Q
**LC 1219 黄金矿工**｜Medium

`grid` 中每格是黄金数量，`0` 表示空。可从任一非空格出发，每次走到相邻（上下左右）的非空格，每格只能采一次，不能走出网格。求最多能采到的黄金数。

## A
**一句话。** 对每个非空格做 DFS 回溯：采完把格子置 `0` 当作已访问，递归后还原，取四个方向的最大值。

```python
def get_maximum_gold(grid):
    m, n = len(grid), len(grid[0])
    def dfs(i, j):
        if not (0 <= i < m and 0 <= j < n):
            return 0
        if grid[i][j] == 0:
            return 0
        gold, grid[i][j] = grid[i][j], 0      # 采走，当作已访问
        best = max(dfs(i + 1, j), dfs(i - 1, j),
                   dfs(i, j + 1), dfs(i, j - 1))
        grid[i][j] = gold                     # 回溯：还原
        return gold + best
    return max(dfs(i, j)
               for i in range(m) for j in range(n))
```

**复杂度。** 时间 `O(mn · 3^k)`（`k` 为非空格数，最多 25），空间 `O(k)`。

**易错点。**
- 回溯后忘了还原：格子被永久置 `0`，其他起点看到的地图是错的。
- 起点只选一个：起点要尝试每个非空格，答案取最大。
- 把 `visited` 另开数组：可以，但直接把格子置 `0` 更省，且天然排除了空格。

**追问。**
- 复杂度为什么是 `3^k`？：除起点外每步最多三个方向可选（不回头），非空格不超过 25 个。
- 能剪枝吗？：只从「度 ≤ 1」的角落格开始，路径端点常在其中，但一般不必。

**同模式。** LC 79 单词搜索、LC 980 不同路径 III

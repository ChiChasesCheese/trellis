---
slug: count-islands-with-total-value-divisible-by-k
---
## Q
**LC 3619 总价值可以被 K 整除的岛屿数目**｜Medium

`grid` 中正整数是陆地，四连通的陆地组成岛屿，岛屿的总价值是格子值之和。统计总价值能被 `k` 整除的岛屿数。

## A
**一句话。** 遇到陆地就 DFS 累加整座岛的价值并把格子清零当作已访问，总价值 `% k == 0` 就计一座。

```python
def count_islands(grid, k):
    m, n = len(grid), len(grid[0])

    def dfs(i, j):      # 返回这座岛尚未统计的价值和
        if not (0 <= i < m and 0 <= j < n):
            return 0
        if grid[i][j] == 0:
            return 0
        total = grid[i][j]
        grid[i][j] = 0  # 清零 = 已访问
        return (total + dfs(i+1, j) + dfs(i-1, j)
                + dfs(i, j+1) + dfs(i, j-1))

    return sum(grid[i][j] > 0 and dfs(i, j) % k == 0
               for i in range(m) for j in range(n))
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 外层把水格也送进 DFS：水格总价值是 `0`，`0 % k == 0`，每个水格都被当成一座岛，示例 1 远大于 `2`。
- 把对角线也当连通：只能上下左右。
- 递归深度可达 `10^5`：`316 x 316` 的全陆地网格就会 `RecursionError`。

**追问。**
- 怎么避免递归爆栈？：改用显式栈 / BFS，入栈时就清零。
- 不想改输入？：另开 `visited` 集合，多 `O(mn)` 空间。

**同模式。** LC 200 岛屿数量、LC 695 岛屿的最大面积、LC 1254 统计封闭岛屿的数目、LC 1020 飞地的数量

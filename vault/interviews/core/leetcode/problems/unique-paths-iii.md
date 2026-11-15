---
slug: unique-paths-iii
---
## Q
**LC 980 不同路径 III**｜Hard

网格里 `1` 是起点，`2` 是终点，`0` 是可走的空格，`-1` 是障碍。统计从起点到终点、四方向移动、恰好经过每个空格一次的路径数。

## A
**一句话。** 回溯 DFS：走过的格子临时标成障碍，到终点时检查是否恰好走完所有空格。

```python
def unique_paths_iii(grid):
    m, n = len(grid), len(grid[0])
    left = 1                     # 还需走的步数 = 空格数 + 1
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0:
                left += 1
            elif grid[i][j] == 1:
                si, sj = i, j
    def dfs(i, j, left):
        if grid[i][j] == 2:
            return int(left == 0)   # 空格必须全走完
        grid[i][j], saved = -1, grid[i][j]   # 标记已走
        cnt = 0
        for x, y in ((i + 1, j), (i - 1, j),
                     (i, j + 1), (i, j - 1)):
            if (0 <= x < m and 0 <= y < n
                    and grid[x][y] != -1):
                cnt += dfs(x, y, left - 1)
        grid[i][j] = saved       # 回溯
        return cnt
    return dfs(si, sj, left)
```

**复杂度。** 时间 `O(3^(mn))`（每步至多三个方向），空间 `O(mn)`。

**易错点。**
- 到终点就记一条路径：必须检查空格是否全走完，否则会多算。
- 回溯时不还原：格子恢复成原值，不能直接写 `0`，否则起点和终点被改坏。
- 把终点当可经过的格子：路径到终点就结束。

**追问。**
- 怎样加速？：用位掩码记走过的格子配合记忆化，状态是（位置，已走集合），这是哈密顿路径的状态压缩 DP。
- 为什么 `left` 要多算 1？：除了每个空格，最后还要有一步踏上终点。

**同模式。** LC 62 不同路径、LC 79 单词搜索、LC 212 单词搜索 II、LC 37 解数独

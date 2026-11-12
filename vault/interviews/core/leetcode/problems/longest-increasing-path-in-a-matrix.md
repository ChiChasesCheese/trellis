---
slug: longest-increasing-path-in-a-matrix
---
## Q
**LC 329 矩阵中的最长递增路径**｜Hard

在整数矩阵中，每步走到上下左右的邻格且值严格递增，求最长路径的格子数。

## A
**一句话。** 「相邻且更大」构成 DAG，记忆化 DFS 求从每格出发的最长路径。

```python
def longest_increasing_path(matrix):
    m, n = len(matrix), len(matrix[0])
    memo = [[0] * n for _ in range(m)]   # 0 表示还没算

    def dfs(i, j):
        if memo[i][j]:
            return memo[i][j]
        best = 1                         # 至少有自己
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if (0 <= x < m and 0 <= y < n
                    and matrix[x][y] > matrix[i][j]):
                best = max(best, 1 + dfs(x, y))
        memo[i][j] = best
        return best

    return max(dfs(i, j)
               for i in range(m) for j in range(n))
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 严格大于写成大于等于：相等邻格成环，`[[5,5],[5,5]]` 抛 `RecursionError`，应为 `1`。
- 把对角线当邻居：示例 `[[3,4,5],[3,2,6],[2,2,1]]` 得 `6`，应为 `4`。
- 递归深度：路径可达两万格，要调高递归上限，且别用 `@cache`（C 栈会先溢出），用手写 `memo`。

**追问。**
- 不想递归怎么办？：拓扑排序，反复剥掉出度为 `0`（比所有邻居都大）的格子，剥的层数就是答案。
- 先排序再 DP？：格子按值升序处理，`len[i][j] = 1 + max(更小邻居)`，`O(mn log mn)`。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 300 最长递增子序列、LC 1857 有向图中最大颜色值

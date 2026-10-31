---
id: tlc-unique-paths-4-followup
node: p3.unique-paths
type: qa
step: 4
---
## Q
**LC 62 不同路径**｜追问

面试官接着问：（1）网格里有障碍物（LC 63）怎么办？（2）`m, n` 到 `10^5` 且答案取模？（3）路径必须经过某个指定格子？（4）表太大怎么办？

## A
1. **障碍物。** 组合公式失效，回到 DP：障碍格的路径数置 `0`，其余照旧：

```python
def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]             # dp[i][j]：走到 (i, j) 的路径数
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                continue                         # 障碍格：到不了，保持 0
            if i == 0 and j == 0:
                dp[i][j] = 1                     # 起点
            else:
                dp[i][j] = (dp[i - 1][j] if i else 0) + (dp[i][j - 1] if j else 0)
    return dp[m - 1][n - 1]
```

`[[0,0,0],[0,1,0],[0,0,0]]` → `2`；`[[0,1],[0,0]]` → `1`；`[[1]]` → `0`。
2. **取模、大范围。** DP 太慢，用组合数：预处理阶乘 `fact` 和逆元 `inv_fact`，`C(m+n-2, m-1) = fact[m+n-2] * inv_fact[m-1] * inv_fact[n-1] % MOD`，`O(m + n)` 预处理，`O(1)` 一次查询。
3. **必经格。** 路径经过 `(a, b)`：起点到 `(a, b)` 的路径数乘以 `(a, b)` 到终点的路径数，两段分别用组合公式。
4. 空间可以压到 O(n)：见 Python 工具箱「DP 降维」。

**Python 提醒**：建二维表要写 `[[0] * n for _ in range(m)]`，写成 `[[0] * n] * m` 会让所有行是同一个列表对象；`math.comb` 在 Python 3.8 以后可用，参数必须是非负整数，`comb(n, k)` 当 `k > n` 时返回 `0`。

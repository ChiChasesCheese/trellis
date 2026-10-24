---
id: tlc-unique-paths-4-followup
node: b.unique-paths
type: qa
step: 4
---
## Q
**LC 62 不同路径**｜追问

面试官接着问：（1）网格里有障碍物（LC 63）怎么办？（2）`m, n` 到 `10^5` 且答案取模？（3）路径必须经过某个指定格子？

## A
1. **障碍物。** 组合公式失效，回到 DP：障碍格的路径数置 `0`，其余照旧。一维滚动：

```python
def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    dp = [0] * len(grid[0])
    dp[0] = 1                                    # 起点的路径数
    for row in grid:
        for j, cell in enumerate(row):
            if cell == 1:
                dp[j] = 0                        # 障碍格：到不了
            elif j:
                dp[j] += dp[j - 1]               # dp[j] 是从上来的，dp[j-1] 是从左来的
    return dp[-1]
```

`[[0,0,0],[0,1,0],[0,0,0]]` → `2`；`[[0,1],[0,0]]` → `1`。
2. **取模、大范围。** DP 太慢，用组合数：预处理阶乘 `fact` 和逆元 `inv_fact`，`C(m+n-2, m-1) = fact[m+n-2] * inv_fact[m-1] * inv_fact[n-1] % MOD`，`O(m + n)` 预处理，`O(1)` 一次查询。
3. **必经格。** 路径经过 `(a, b)`：起点到 `(a, b)` 的路径数乘以 `(a, b)` 到终点的路径数，两段分别用组合公式。

**Python 提醒**：`itertools.accumulate` 返回迭代器，要滚动复用必须 `list(...)`；`math.comb` 在 Python 3.8 以后可用，参数必须是非负整数，`comb(n, k)` 当 `k > n` 时返回 `0`。

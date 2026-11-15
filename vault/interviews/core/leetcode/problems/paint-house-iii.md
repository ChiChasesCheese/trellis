---
slug: paint-house-iii
---
## Q
**LC 1473 粉刷房子 III**｜Hard

一排 `m` 个房子、`n` 种颜色，`houses[i] = 0` 表示未涂，否则颜色已定不能改；`cost[i][j]` 是把房子 `i` 涂成颜色 `j+1` 的花费。连续同色是一个街区，求恰好 `target` 个街区的最小花费，做不到返回 `-1`。

## A
**一句话。** 三维 DP `f[i][j][c]`：前 `i+1` 个房子组成 `j` 个街区、第 `i` 个为颜色 `c` 的最小花费；同色接上街区数不变，异色街区数加一。

```python
def min_cost(houses, cost, m, n, target):
    # f[i][j][c]：到第 i 个房子，j 个街区，i 的颜色为 c
    f = [[[inf] * (n + 1) for _ in range(target + 1)]
         for _ in range(m)]
    for i in range(m):
        given = houses[i]
        for c in [given] if given else range(1, n + 1):
            pay = 0 if given else cost[i][c - 1]
            if i == 0:
                f[0][1][c] = pay
                continue
            for j in range(1, target + 1):
                same = f[i - 1][j][c]          # 接上同色街区
                diff = min((f[i - 1][j - 1][d]  # 开新街区
                            for d in range(1, n + 1)
                            if d != c), default=inf)
                f[i][j][c] = min(same, diff) + pay
    ans = min(f[m - 1][target])
    return -1 if ans == inf else ans
```

**复杂度。** 时间 `O(m·target·n²)`，空间 `O(m·target·n)`。

**易错点。**
- 已涂色的房子也付钱：`houses[i] != 0` 时花费为 0，且只能取这一种颜色。
- 只有一种颜色时求异色最小值：`min` 遇到空序列会抛错，要给 `default=inf`。

**追问。**
- 去掉一个 `n`？：对每个 `(i-1, j-1)` 预先求最小值和次小值，异色转移 `O(1)`，总 `O(m·target·n)`。
- 空间优化？：只依赖上一行，滚动成两层；卡片里保留完整表便于看清状态。

**同模式。** LC 188 买卖股票的最佳时机 IV、LC 256 粉刷房子、LC 265 粉刷房子 II

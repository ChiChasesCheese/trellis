---
id: tlc-patterns-dp-knapsack-5-egg-drop
node: patterns.dp-knapsack
type: qa
step: 5
---
## Q
**动态规划：背包与计数｜鸡蛋掉落（LC 887）：把"求最少步数"反过来变成"求最多楼层"**

`k` 个鸡蛋、`n` 层楼，最少扔几次能确定临界楼层？为什么 `O(k n^2)` 的 DP 不够，反过来的状态怎么设？

## A
朴素 DP：`f(k, n) = 1 + min over x of max(f(k-1, x-1), f(k, n-x))`（在第 `x` 层扔：碎了往下找，没碎往上找），复杂度 `O(k n^2)`，`n = 10^4` 太慢。

**反过来**：令 `dp[m][j]` = 用 `j` 个蛋、最多扔 `m` 次，**最多能确定多少层楼**。扔一次：蛋碎了，下面还能确定 `dp[m-1][j-1]` 层；没碎，上面还能确定 `dp[m-1][j]` 层；再加当前这一层：

`dp[m][j] = dp[m-1][j-1] + dp[m-1][j] + 1`

找最小的 `m` 使得 `dp[m][k] >= n`。

```python
def super_egg_drop(k: int, n: int) -> int:
    # dp[m][j]：用 j 个蛋、最多扔 m 次，最多能确定的楼层数；第 0 行：0 次什么也确定不了
    dp = [[0] * (k + 1)]
    while dp[-1][k] < n:
        m = len(dp)                        # 要填的新一行：扔 m 次
        dp.append([0] * (k + 1))           # dp[m][0] = 0：没有蛋什么也确定不了
        for j in range(1, k + 1):
            dp[m][j] = dp[m - 1][j - 1] + dp[m - 1][j] + 1     # 只读上一行
    return len(dp) - 1                     # 第一次 dp[m][k] >= n 的行号 m
print(super_egg_drop(1, 2), super_egg_drop(2, 6), super_egg_drop(3, 14), super_egg_drop(100, 10000))   # 2 3 4 14
```

- 时间 `O(k · m)`，空间 `O(k · m)`；`m` 最多约 `log n`（蛋足够时）或 `n`（只有一个蛋时 `m = n`），实际在 `k = 100`、`n = 10^4` 时只有 `15` 行，几乎瞬间完成。
- 每一格只读上一行 `dp[m-1]`，与 0-1 背包读上一行的理由相同；空间可以压到 O(k)：见 Python 工具箱「DP 降维」。
- 本质是二项式和：`dp[m][k] = sum(C(m, i) for i in 1..k)`；`k = 2, m = 3` 时 `3 + 3 = 6`，对应 `n = 6` 需要 3 次。
- 也可以对 `m` 二分查找，再用上面的公式检查 `dp >= n`。

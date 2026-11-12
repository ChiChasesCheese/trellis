---
slug: coin-change
---
## Q
**LC 322 零钱兑换**｜Medium

给面额数组 `coins`（每种数量无限）和金额 `amount`，求凑成 `amount` 的最少硬币数，凑不出返回 `-1`。

## A
**一句话。** 完全背包（unbounded knapsack）求最小值：`dp[a] = min(dp[a-c] + 1)`，外层硬币、内层金额正序。

```python
def coin_change(coins, amount):
    inf = amount + 1              # 哨兵：比任何真实答案都大
    dp = [0] + [inf] * amount     # dp[a]：凑成 a 的最少硬币数
    for c in coins:
        for a in range(c, amount + 1):   # 正序：同一枚可重复
            dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] < inf else -1
```

**复杂度。** 时间 `O(amount × len(coins))`，空间 `O(amount)`。

**易错点。**
- 贪心取最大面额：`[1,3,4]`、`amount=6` 贪心得 `4+1+1` 三枚，应为 `3+3` 两枚。
- 内层金额倒序：变成 0/1 背包，`[2]`、`amount=4` 得 `-1`，应为 `2`。
- 哨兵用 `0` 或 `-1`：会被 `min` 当成真实答案。

**追问。**
- 统计组合数（LC 518）？：`dp[a] += dp[a-c]`，外层硬币；内外层对调就成了排列数（LC 377）。
- 要输出用了哪些硬币？：另存 `pick[a]` 记最后一枚，从 `amount` 回溯。

**同模式。** LC 518 零钱兑换 II、LC 377 组合总和 IV、LC 279 完全平方数、LC 139 单词拆分

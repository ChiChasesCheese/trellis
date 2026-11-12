---
slug: coin-change-ii
---
## Q
**LC 518 零钱兑换 II**｜Medium

给不同面额的硬币 `coins`（每种无限个）和金额 `amount`，求凑成该金额的组合数。

## A
**一句话。** 完全背包数组合：`dp[i][a]` 是只用前 `i` 种硬币凑 `a` 的组合数，读同一行表示可重复用。

```python
def change(amount, coins):
    m = len(coins)
    dp = [[0] * (amount + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1                    # 凑 0 元：什么都不拿
    for i, coin in enumerate(coins, 1):
        for a in range(1, amount + 1):
            dp[i][a] = dp[i - 1][a]     # 不用第 i 种
            if a >= coin:
                dp[i][a] += dp[i][a - coin]   # 再用一枚（同一行）
    return dp[m][amount]
```

**复杂度。** 时间 `O(n·amount)`，空间 `O(n·amount)`。

**易错点。**
- 转移读上一行 `dp[i-1][a-coin]`：变成 0/1 背包，`(5,[1,2,5])` 得 `1`，应为 `4`。
- 第 0 列没置 `1`：`(0,[7])` 得 `0`，应为 `1`。
- 漏掉 `a >= coin`：负下标从行尾读数，`(1,[3])` 得 `1`，应为 `0`。

**追问。**
- 数排列而不是组合（LC 377）？：外层金额、内层硬币，两层循环互换。
- 空间能压吗？：压成一维 `O(amount)`，内层金额必须正序，倒序就成了 0/1 背包。

**同模式。** LC 322 零钱兑换、LC 377 组合总和 IV、LC 279 完全平方数、LC 494 目标和

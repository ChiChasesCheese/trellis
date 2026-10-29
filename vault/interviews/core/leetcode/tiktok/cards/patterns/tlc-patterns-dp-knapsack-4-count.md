---
id: tlc-patterns-dp-knapsack-4-count
node: patterns.dp-knapsack
type: qa
step: 4
---
## Q
**动态规划：背包与计数｜计数背包：组合数与排列数的区别**

凑出金额的"组合数"和"排列数"在循环顺序上有什么区别？

## A
**组合数（顺序无关）**：**外层遍历物品，内层遍历容量**，同一个组合只出现一次。

```python
def coin_change_ii(amount: int, coins: list[int]) -> int:
    n = len(coins)
    dp = [[0] * (amount + 1) for _ in range(n + 1)]   # dp[i][a]：前 i 种凑出 a 的组合数
    dp[0][0] = 1                           # 空组合
    for i in range(1, n + 1):
        for a in range(amount + 1):
            dp[i][a] = dp[i - 1][a]        # 不用第 i 种
            if a >= coins[i - 1]:
                dp[i][a] += dp[i][a - coins[i - 1]]   # 用第 i 种：读本行
    return dp[n][amount]


def permutation_count(amount: int, coins: list[int]) -> int:
    dp = [1] + [0] * amount                # 状态只有金额
    for a in range(1, amount + 1):         # 外层遍历金额
        for coin in coins:
            if coin <= a:
                dp[a] += dp[a - coin]
    return dp[amount]
print(coin_change_ii(3, [1, 2]), permutation_count(3, [1, 2]))   # 2 3
```

`amount = 3`、`[1, 2]`：组合 `2` 个，排列还区分 `1+2` 与 `2+1`，共 `3` 个；`coin_change_ii(5, [1,2,5])` → `4`。

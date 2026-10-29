---
id: tlc-coin-change-ii-2-code
node: a.coin-change-ii
type: qa
step: 2
---
## Q
**LC 518 零钱兑换 II**｜写出 Python 实现

`coins` 是 `1` 到 `300` 个互不相同的面额（每个在 `[1, 5000]`），`amount` 在 `[0, 5000]`，每种硬币有无限个。返回凑成 `amount` 的硬币组合数，凑不出返回 `0`。

## A
**思路。** `dp[i][a]` 是只用前 `i` 种硬币凑出金额 `a` 的组合数。第 0 列都是 `1`（凑 `0` 元只有一种：什么都不拿），第 0 行其余是 `0`（没有硬币凑不出正金额）。逐行填：不用第 `i` 种是 `dp[i-1][a]`，至少用一枚是 `dp[i][a - coin]`（同一行，剩下的仍可再用第 `i` 种），两者相加。答案是 `dp[n][amount]`。

```python
def change(amount: int, coins: list[int]) -> int:
    m = len(coins)
    # dp[i][a]：只用前 i 种硬币，凑出金额 a 的组合数
    dp = [[0] * (amount + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1                        # 凑出 0 元只有一种：什么都不拿
    for i, coin in enumerate(coins, 1):
        for a in range(1, amount + 1):
            dp[i][a] = dp[i - 1][a]         # 不用第 i 种
            if a >= coin:
                dp[i][a] += dp[i][a - coin]  # 至少用一枚：剩下的仍可再用第 i 种（同一行）
    return dp[m][amount]
```

运行：`(5, [1,2,5])` → `4`，`(3, [2])` → `0`，`(10, [10])` → `1`，`(0, [7])` → `1`。

**复杂度。** 时间 `O(n · amount)`，约 `1.5 * 10^6` 次加法；空间 `O(n · amount)`：`(n + 1) × (amount + 1)` 的表。

**写法要点。** `[[0] * (amount + 1) for _ in range(m + 1)]` 每行是一个新列表；`enumerate(coins, 1)` 让 `i` 直接是「前 `i` 种」的行号，`coin` 是第 `i` 种面额，不用写 `coins[i - 1]`；`if a >= coin` 保证 `a - coin` 不会变成负下标（Python 的负下标不会报错，而是悄悄读到行尾）；同一行的 `dp[i][a - coin]` 在 `a` 从小到大填时已经算好，所以不需要任何方向技巧；`amount = 0` 时内层循环为空，直接返回 `dp[m][0] = 1`。

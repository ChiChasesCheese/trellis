---
id: tlc-coin-change-2-code
node: b.coin-change
type: qa
step: 2
---
## Q
**LC 322 零钱兑换**｜写出 Python 实现

整数数组 `coins`（长度 `1` 到 `12`，面额在 `1` 到 `2^31 - 1`）和整数 `amount`（`0` 到 `10^4`），每种硬币无限个，返回凑成 `amount` 的最少硬币数，凑不出返回 `-1`。

## A
**思路。** `dp[a]` 表示凑成金额 `a` 的最少硬币数，`dp[0] = 0`，其余初值是哨兵 `amount + 1`。外层遍历每种硬币，内层金额从小到大，用 `dp[a - c] + 1` 更新 `dp[a]`。

```python
def coin_change(coins: list[int], amount: int) -> int:
    inf = amount + 1                      # 哨兵：比任何真实答案都大
    dp = [0] + [inf] * amount             # dp[a] = 凑成金额 a 的最少硬币数
    for c in coins:                       # 完全背包：外层硬币，内层金额正序（同一枚硬币可重复用）
        for a in range(c, amount + 1):
            dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] < inf else -1
```

运行：`([1,2,5], 11)` → `3`，`([2], 3)` → `-1`，`([1], 0)` → `0`，`([1,3,4], 6)` → `2`，`([186,419,83,408], 6249)` → `20`，`([2147483647], 10000)` → `-1`。

**复杂度。** 时间 `O(amount × len(coins))`：每个硬币扫一遍金额；空间 `O(amount)`：一维数组。

**写法要点。** `[0] + [inf] * amount` 一行建好整个表，`dp[0]` 是边界；`range(c, amount + 1)` 让大于金额的硬币自动跳过，不用写 `if c <= a`；哨兵 `amount + 1` 用整数而不是 `float('inf')`，全程整数运算，类型一致；循环顺序「硬币在外、金额在内、正序」就是完全背包的模板，倒序则是 0/1 背包。

---
id: tlc-patterns-dp-knapsack-2-template
node: patterns.dp-knapsack
type: qa
step: 2
---
## Q
**动态规划：背包与计数｜模板：0-1 背包（分割等和子集）与完全背包（零钱兑换）**

写出两个一维背包的标准写法，说明容量循环方向的区别。

## A
```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [False] * (target + 1)            # dp[s]：能否选出一些数，和恰好为 s
    dp[0] = True
    for x in nums:
        for s in range(target, x - 1, -1): # 0-1 背包：容量从大到小，每个数最多用一次
            dp[s] = dp[s] or dp[s - x]
    return dp[target]

def coin_change(coins: list[int], amount: int) -> int:
    inf = amount + 1                       # 比任何合法答案都大的哨兵
    dp = [0] + [inf] * amount              # dp[a]：凑出金额 a 的最少硬币数
    for coin in coins:
        for a in range(coin, amount + 1):  # 完全背包：容量从小到大，同一种硬币可重复用
            dp[a] = min(dp[a], dp[a - coin] + 1)
    return -1 if dp[amount] >= inf else dp[amount]
```

运行：`can_partition([1,5,11,5])` → `True`；`[1,2,3,5]` → `False`；`[2]` → `False`。`coin_change([1,2,5], 11)` → `3`；`([2], 3)` → `-1`；`([1], 0)` → `0`；`([186,419,83,408], 6249)` → `20`。

| | 0-1 背包 | 完全背包 |
|---|---|---|
| 每个物品 | 最多用 1 次 | 可用无限次 |
| 容量循环 | **从大到小** | **从小到大** |
| 原因 | `dp[s - x]` 必须是"还没用过 `x`"的旧值 | `dp[a - coin]` 可以是"已经用过 `coin`"的新值 |

- 时间 `O(n · 容量)`，空间 `O(容量)`。
- 凑不出时 `dp[a]` 保持哨兵值；用 `inf = amount + 1` 而不是 `float('inf')` 可以保持整数类型。
- 二维表 `dp[i][s]` 是一维的原型：一维数组等价于二维表"滚动掉第一维"。

---
id: tlc-patterns-dp-knapsack-2-template
node: patterns.dp-knapsack
type: qa
step: 2
---
## Q
**动态规划：背包与计数｜模板：0-1 背包（分割等和子集）与完全背包（零钱兑换）**

写出两个背包的完整二维表写法，说明 0-1 背包和完全背包的转移分别读哪一行。

## A
```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    n, target = len(nums), total // 2
    dp = [[False] * (target + 1) for _ in range(n + 1)]   # dp[i][s]：前 i 个数能否凑出和 s
    dp[0][0] = True                        # 基础行：一个数都不选，只能凑出 0
    for i in range(1, n + 1):
        x = nums[i - 1]
        for s in range(target + 1):
            dp[i][s] = dp[i - 1][s] or (s >= x and dp[i - 1][s - x])   # 选第 i 个：读上一行
    return dp[n][target]


def coin_change(coins: list[int], amount: int) -> int:
    n = len(coins)
    inf = amount + 1                       # 哨兵：比任何合法答案都大
    dp = [[inf] * (amount + 1) for _ in range(n + 1)]     # dp[i][a]：前 i 种硬币凑出 a 的最少枚数
    dp[0][0] = 0                           # 基础行：一种硬币都不用，只能凑出 0
    for i in range(1, n + 1):
        for a in range(amount + 1):
            dp[i][a] = dp[i - 1][a]        # 不用第 i 种
            if a >= coins[i - 1]:
                dp[i][a] = min(dp[i][a], dp[i][a - coins[i - 1]] + 1)   # 用第 i 种：读本行
    return -1 if dp[n][amount] >= inf else dp[n][amount]
```

运行：`can_partition([1,5,11,5])` → `True`；`[1,2,3,5]` → `False`；`[2]` → `False`。`coin_change([1,2,5], 11)` → `3`；`([2], 3)` → `-1`；`([1], 0)` → `0`；`([186,419,83,408], 6249)` → `20`。

| | 0-1 背包 | 完全背包 |
|---|---|---|
| 每个物品 | 最多用 1 次 | 可用无限次 |
| 转移读 | **上一行** `dp[i-1]` | **本行** `dp[i]` |
| 原因 | 上一行还没用过第 `i` 个 | 本行已允许用第 `i` 种，再加一枚就是重复 |

- 时间、空间都是 `O(n · 容量)`；空间可以压到 O(容量)：见 Python 工具箱「DP 降维」。

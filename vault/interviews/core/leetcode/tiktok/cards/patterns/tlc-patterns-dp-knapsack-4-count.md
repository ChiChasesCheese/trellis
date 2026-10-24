---
id: tlc-patterns-dp-knapsack-4-count
node: patterns.dp-knapsack
type: qa
step: 4
---
## Q
**动态规划：背包与计数｜计数背包：组合数与排列数的区别，以及"目标和"**

凑出金额的"组合数"和"排列数"在循环顺序上有什么区别？目标和（给每个数加 `+` / `-`）怎样转成背包？

## A
**组合数（顺序无关）**：**外层遍历物品，内层遍历容量**。每种硬币按固定顺序一次性处理完，同一个组合只会出现一次。

```python
def coin_change_ii(amount: int, coins: list[int]) -> int:
    dp = [1] + [0] * amount                # dp[a]：凑出 a 的组合数
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
    return dp[amount]

def permutation_count(amount: int, coins: list[int]) -> int:
    dp = [1] + [0] * amount
    for a in range(1, amount + 1):         # 外层遍历金额：不同顺序算不同方案
        for coin in coins:
            if coin <= a:
                dp[a] += dp[a - coin]
    return dp[amount]
print(coin_change_ii(3, [1, 2]), permutation_count(3, [1, 2]))   # 2 3
```

`amount = 3`、硬币 `[1, 2]`：组合是 `{1,1,1}`、`{1,2}`，共 `2` 个；排列还要区分 `1+2` 与 `2+1`，共 `3` 个。`coin_change_ii(5, [1,2,5])` → `4`。

**目标和（LC 494）**：给每个数前面加 `+` 或 `-`，结果为 `target`。设取 `+` 的数之和为 `P`，总和为 `S`：`P - (S - P) = target`，`P = (S + target) / 2`。问题变成"选一部分数使和为 `P`"的 0-1 计数背包。

```python
def find_target_sum_ways(nums: list[int], target: int) -> int:
    total = sum(nums)
    if abs(target) > total or (total + target) % 2:
        return 0
    want = (total + target) // 2
    dp = [1] + [0] * want
    for x in nums:
        for s in range(want, x - 1, -1):   # 0-1：倒序
            dp[s] += dp[s - x]
    return dp[want]
print(find_target_sum_ways([1, 1, 1, 1, 1], 3), find_target_sum_ways([1], 2), find_target_sum_ways([0, 0, 1], 1))   # 5 0 4
```

含 `0` 的数组：每个 `0` 可以取 `+` 或 `-`，使方案数翻倍，上面的写法自然处理。

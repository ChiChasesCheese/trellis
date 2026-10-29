---
id: tlc-python-dp-space-compression-4-knapsack-direction
node: python.dp-space-compression
type: qa
step: 4
---
## Q
**DP 降维｜0-1 背包倒序，完全背包正序**

分割等和子集（LC 416）为什么容量倒序，零钱兑换 II（LC 518）为什么正序？方向写反各会得到什么？

## A
二维表里，0-1 背包读**上一行**：`dp[i][s]` 用 `dp[i-1][s-x]`，每个物品一次；完全背包读**本行**：`dp[i][a]` 用 `dp[i][a-coin]`，同一种硬币可重复。压成一行后，上一行的值是旧值，本行的值是新值。

```python
def count_ways(items: list[int], target: int, backward: bool) -> int:
    dp = [1] + [0] * target                 # dp[s]：凑出 s 的方案数
    for w in items:
        cols = range(target, w - 1, -1) if backward else range(w, target + 1)
        for s in cols:
            dp[s] += dp[s - w]              # dp[s - w] 在 s 左边
    return dp[target]

print(count_ways([1, 5], 3, True), count_ways([1, 5], 3, False))        # 0 1
print(count_ways([1, 2, 5], 5, True), count_ways([1, 2, 5], 5, False))  # 1 4
```

- 0-1（LC 416）要倒序：`dp[s-w]` 在左边，倒序时还没被覆盖，是旧值。`[1, 5]` 凑 `3`：倒序得 `0`（正确，凑不出）；正序得 `1`，同一个 `1` 被用了三次。
- 完全（LC 518）要正序：`dp[s-w]` 必须已被覆盖，是新值。`amount = 5`、`[1, 2, 5]`：正序得 `4`（正确）；倒序得 `1`，每种硬币只能用一次，只剩 `{5}`。
- 口诀：0-1 倒序，完全正序；先问"每个物品能用几次"。
- LC 416 只问能否，把 `+=` 换成 `dp[s] = dp[s] or dp[s - w]`，方向不变。

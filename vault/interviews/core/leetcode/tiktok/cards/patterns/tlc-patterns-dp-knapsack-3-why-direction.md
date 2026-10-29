---
id: tlc-patterns-dp-knapsack-3-why-direction
node: patterns.dp-knapsack
type: qa
step: 3
---
## Q
**动态规划：背包与计数｜正确性：0-1 背包读上一行，完全背包读本行，及计数版（目标和）**

把分割等和子集的转移改成读本行会错在哪里？完全背包为什么恰好要读本行？0-1 的计数版本（目标和，LC 494）怎么写？

## A
**两行的含义**：`dp[i-1][·]` 是"只用前 `i-1` 个物品"，`dp[i][·]` 是"可以用前 `i` 个物品"。

- **0-1 背包读上一行**：`dp[i][s]` 的"选第 `i` 个数"分支是 `dp[i-1][s - x]`——前面的方案里还没有第 `i` 个数，加上它恰好一次。
- **读本行**：`dp[i][s - x]` 可能已经包含第 `i` 个数，再加一次 `x`，同一个数被用了多次，变成完全背包。

**反例**：`nums = [1, 5]`，总和 `6`，`target = 3`。
- 读本行的写法 `dp[i][s] = dp[i-1][s] or dp[i][s-x]`：第 `1` 行 `x = 1`，`dp[1][1]` 由 `dp[0][0]` 得到（用 `1`），`dp[1][2]` 由 `dp[1][1]` 得到（又用了一次 `1`），`dp[1][3]` 由 `dp[1][2]` 得到，`dp[2][3]` 继承它，返回 `True`。
- 实际上 `1` 只有一个，无法凑出 `3`，正确答案 `False`。

**反过来，完全背包必须读本行**：`coin_change([1, 2, 5], 11)` 要允许同一种硬币重复用，读本行的 `dp[i][a - coin]` 已包含"用过这种硬币"。若误读上一行，每种硬币只能用一次，最多凑出 `1 + 2 + 5 = 8`，`11` 凑不出，返回 `-1`，正确是 `3`。

- 记忆口诀：**0-1 读上一行，完全读本行**；遇到新题先问"每个物品能用几次"。
- 二维表的写法一眼就能看出读的是哪一行，不用记方向；空间 `O(n · 容量)`。压成一维数组后，"读上一行"和"读本行"分别变成容量倒序和正序：见 Python 工具箱「DP 降维」。

**目标和（LC 494）**：每个数加 `+` 或 `-`，结果为 `target`。取 `+` 的数之和为 `P`，总和 `S`：`P - (S - P) = target`，`P = (S + target) / 2`，变成 0-1 计数背包。

```python
def find_target_sum_ways(nums: list[int], target: int) -> int:
    total = sum(nums)
    if abs(target) > total or (total + target) % 2:
        return 0
    n, want = len(nums), (total + target) // 2
    dp = [[0] * (want + 1) for _ in range(n + 1)]     # dp[i][s]：前 i 个数和为 s 的方案数
    dp[0][0] = 1                           # 都不选
    for i in range(1, n + 1):
        for s in range(want + 1):
            dp[i][s] = dp[i - 1][s]        # 第 i 个数取 -
            if s >= nums[i - 1]:
                dp[i][s] += dp[i - 1][s - nums[i - 1]]   # 取 +：读上一行
    return dp[n][want]
print(find_target_sum_ways([1, 1, 1, 1, 1], 3), find_target_sum_ways([1], 2), find_target_sum_ways([0, 0, 1], 1))   # 5 0 4
```

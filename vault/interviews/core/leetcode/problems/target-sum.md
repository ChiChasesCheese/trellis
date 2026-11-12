---
slug: target-sum
---
## Q
**LC 494 目标和**｜Medium

给非负整数数组 `nums`，每个数前加 `+` 或 `-`，求结果等于 `target` 的表达式个数。

## A
**一句话。** 设取 `+` 的子集和为 `P = (总和 + target) / 2`，转成 01 背包计数 `dp[i][j]`。

```python
def find_target_sum_ways(nums, target):
    need, odd = divmod(sum(nums) + target, 2)
    if odd or need < 0:
        return 0
    n = len(nums)
    # dp[i][j]：前 i 个数里选若干个、和恰为 j 的方案数
    dp = [[0] * (need + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for i, x in enumerate(nums, 1):
        for j in range(need + 1):
            dp[i][j] = dp[i - 1][j]            # 不选
            if j >= x:
                dp[i][j] += dp[i - 1][j - x]   # 选，只读上一行
    return dp[n][need]
```

**复杂度。** 时间 `O(n · P)`，空间 `O(n · P)`。

**易错点。**
- 转移读了同一行 `dp[i][j-x]`：变成完全背包，`[1,1,1,1,1]`、`3` 得 `70`，应为 `5`。
- 不判奇偶和 `need < 0`：`[1,1]`、`target = -3` 时 `need = -1`，建表后 `IndexError`。
- 过滤掉 `0`：每个 `0` 前 `+` / `-` 是两种表达式，方案数翻倍，`[0,0,0,0,0,0,0,0,1]`、`1` 应为 `256`。

**追问。**
- 元素有负数怎么办？：变换不成立，改用字典记每步可达的和及方案数。
- `n <= 20` 但和很大？：折半枚举（meet in the middle），两半各 `2^10` 个和，用字典配对。

**同模式。** LC 416 分割等和子集、LC 1049 最后一块石头的重量 II、LC 474 一和零、LC 518 零钱兑换 II

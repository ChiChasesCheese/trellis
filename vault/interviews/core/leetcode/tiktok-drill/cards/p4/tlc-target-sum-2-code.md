---
id: tlc-target-sum-2-code
node: p4.target-sum
type: qa
step: 2
---
## Q
**LC 494 目标和**｜写出 Python 实现

非负整数数组 `nums`（`1 <= nums.length <= 20`，`0 <= nums[i] <= 1000`，`sum(nums) <= 1000`）和整数 `target`（`-1000 <= target <= 1000`）。给每个数前添加 `+` 或 `-`，返回结果等于 `target` 的不同表达式的数目。

## A
**思路。** 加号那堆的和 `P = (sum + target) / 2`。如果这个值不是非负整数，或 `target` 超出 `[-sum, sum]`，返回 `0`；否则用 01 背包数出和为 `P` 的子集个数：`dp[i][j]` 是从前 `i` 个数里选若干个、和恰为 `j` 的方案数，第 0 行只有 `dp[0][0] = 1`，第 `i` 行是「不选」`dp[i-1][j]` 加上「选」`dp[i-1][j-x]`。

```python
def find_target_sum_ways(nums: list[int], target: int) -> int:
    total = sum(nums)
    need, odd = divmod(total + target, 2)    # 正数子集之和 P = (total + target) / 2
    if odd or need < 0 or target > total:    # 奇偶不对，或 target 超出 [-total, total]，直接无解
        return 0
    n = len(nums)
    # dp[i][j]：从前 i 个数里选若干个、和恰为 j 的方案数
    dp = [[0] * (need + 1) for _ in range(n + 1)]
    dp[0][0] = 1                             # 一个数都不选，和为 0：一种
    for i, x in enumerate(nums, 1):
        for j in range(need + 1):
            dp[i][j] = dp[i - 1][j]          # 不选第 i 个
            if j >= x:
                dp[i][j] += dp[i - 1][j - x]  # 选第 i 个：只能从上一行转移，所以每个数只用一次
    return dp[n][need]
```

运行：`[1,1,1,1,1]`，`3` → `5`；`[1]`，`1` → `1`；`[1,2]`，`4` → `0`；`[1,1]`，`-3` → `0`；`[0,0,0,0,0,0,0,0,1]`，`1` → `256`；`[0]`，`0` → `2`。

**复杂度。** 时间 `O(n * P)`，`P = (sum + target) / 2 <= 1000`；空间 `O(n * P)`：`(n + 1) × (P + 1)` 的表。

**写法要点。** `divmod` 一次得到商和余数，奇偶判断顺手完成；`[[0] * (need + 1) for _ in range(n + 1)]` 每行是新列表；`enumerate(nums, 1)` 让 `i` 直接是「前 `i` 个数」的行号，`x` 是第 `i` 个数；转移读的是上一行 `dp[i - 1][j - x]`，所以每个数只用一次，不需要关心 `j` 的遍历方向；`x = 0` 时 `j >= x` 恒成立，`dp[i][j] = dp[i-1][j] + dp[i-1][j]` 让方案数翻倍，正好对应 `+0` 和 `-0` 两种表达式，不需要特判。

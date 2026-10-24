---
id: tlc-target-sum-2-code
node: a.target-sum
type: qa
step: 2
---
## Q
**LC 494 目标和**｜写出 Python 实现

非负整数数组 `nums`（`1 <= nums.length <= 20`，`0 <= nums[i] <= 1000`，`sum(nums) <= 1000`）和整数 `target`（`-1000 <= target <= 1000`）。给每个数前添加 `+` 或 `-`，返回结果等于 `target` 的不同表达式的数目。

## A
**思路。** 加号那堆的和 `P = (sum + target) / 2`。如果这个值不是非负整数，或 `target` 超出 `[-sum, sum]`，返回 `0`；否则用 01 背包数出和为 `P` 的子集个数，容量倒序更新。

```python
def find_target_sum_ways(nums: list[int], target: int) -> int:
    total = sum(nums)
    need, odd = divmod(total + target, 2)    # 正数子集之和 P = (total + target) / 2
    if odd or need < 0 or target > total:    # 奇偶不对，或 target 超出 [-total, total]，直接无解
        return 0
    dp = [0] * (need + 1)                    # dp[j]：选出若干数、和恰为 j 的方案数
    dp[0] = 1
    for x in nums:
        for j in range(need, x - 1, -1):     # 倒序：每个数只用一次；x = 0 时 dp[j] += dp[j] 恰好翻倍
            dp[j] += dp[j - x]
    return dp[need]
```

运行：`[1,1,1,1,1]`，`3` → `5`；`[1]`，`1` → `1`；`[1,2]`，`4` → `0`；`[1,1]`，`-3` → `0`；`[0,0,0,0,0,0,0,0,1]`，`1` → `256`；`[0]`，`0` → `2`。

**复杂度。** 时间 `O(n * P)`，`P = (sum + target) / 2 <= 1000`；空间 `O(P)`。

**写法要点。** `divmod` 一次得到商和余数，奇偶判断顺手完成；`range(need, x - 1, -1)` 倒序保证 `dp[j - x]` 还是上一轮的值，每个数只用一次；`x = 0` 时区间是 `need..0`，`dp[j] += dp[j]` 让方案数翻倍，正好对应 `+0` 和 `-0` 两种表达式，不需要特判。

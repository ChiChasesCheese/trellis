---
id: tlc-greatest-sum-divisible-by-three-2-code
node: a.greatest-sum-divisible-by-three
type: qa
step: 2
---
## Q
**LC 1262 可被三整除的最大和**｜Medium · 字节高频｜写出 Python 实现

整数数组 `nums`（`1 <= nums.length <= 4 * 10^4`，`1 <= nums[i] <= 10^4`），选出一些数（可以不选）使和被 `3` 整除，返回最大和。用完整的二维 DP 表，行是前 `i` 个数，列是余数。

## A
**思路。** `dp[i][r]` 表示只用前 `i` 个数、和模 `3` 等于 `r` 的最大和，不可达记一个很小的负数。第 `i` 个数 `x`：不选则继承 `dp[i - 1][r]`；选则加在余数为 `(r - x) % 3` 的状态上。`dp[0]` 里只有余数 `0` 可达（空集，和为 `0`）。

```python
def max_sum_div_three(nums: list[int]) -> int:
    n = len(nums)
    NEG = -(10 ** 18)                          # 「这个余数凑不出来」
    # dp[i][r]：只用前 i 个数、和模 3 等于 r 时的最大和
    dp = [[NEG] * 3 for _ in range(n + 1)]
    dp[0][0] = 0                               # 空集：和为 0，余数 0
    for i, x in enumerate(nums, 1):
        for r in range(3):
            dp[i][r] = max(dp[i - 1][r],                         # 不选 x
                           dp[i - 1][(r - x) % 3] + x)           # 选 x：上一个余数是 (r - x) % 3
    return dp[n][0]
```

运行：`[3,6,5,1,8]` → `18`，`[4]` → `0`，`[1,2,3,4,4]` → `12`，`[2,2,2,2,2]` → `6`，`[1]` → `0`。

**复杂度。** 时间 `O(n)`：`3n` 个状态，每个常数时间；空间 `O(n)`：`(n + 1) × 3` 的表。

**写法要点。** `enumerate(nums, 1)` 让 `i` 从 `1` 开始，和 `dp[i - 1]` 对得上；`[[NEG] * 3 for _ in range(n + 1)]` 每行单独创建，不会共享同一个内层列表；`max` 比较「选」与「不选」两个候选；`NEG` 用 `-(10 ** 18)` 而不是浮点 `-inf`，整个表保持 `int`，返回值类型是 `int`。

---
id: tlc-continuous-subarray-sum-2-code
node: b.continuous-subarray-sum
type: qa
step: 2
---
## Q
**LC 523 连续的子数组和**｜写出 Python 实现

整数数组 `nums`（`1 <= nums.length <= 10^5`，`0 <= nums[i] <= 10^9`）和整数 `k`（`1 <= k <= 2^31 - 1`），判断是否存在长度至少为 2、元素和为 `k` 的倍数的连续子数组。

## A
**思路。** 维护前缀和对 `k` 的余数。字典记每个余数第一次出现的下标，空前缀的余数 0 对应下标 -1。每步算出新余数，查它最早出现的位置，下标差不小于 2 就返回 `true`。

```python
def check_subarray_sum(nums: list[int], k: int) -> bool:
    first_seen: dict[int, int] = {0: -1}     # 余数 -> 最早出现的前缀下标；空前缀的余数是 0
    prefix = 0
    for i, x in enumerate(nums):
        prefix = (prefix + x) % k            # 到 nums[i] 为止的前缀和对 k 的余数
        j = first_seen.setdefault(prefix, i)  # 第一次出现就登记 i，否则返回最早的下标
        if i - j >= 2:                       # 子数组 nums[j+1 .. i] 的长度 = i - j
            return True
    return False
```

运行：`[23,2,4,6,7], 6` → `true`，`[23,2,6,4,7], 6` → `true`，`[23,2,6,4,7], 13` → `false`，`[5,0,0], 7` → `true`，`[6,1], 6` → `false`，`[0], 1` → `false`。

**复杂度。** 时间 `O(n)`；空间 `O(min(n, k))`。

**写法要点。** `dict.setdefault(prefix, i)` 一步完成「第一次出现就登记，否则取回旧值」，省掉 `if prefix in …` 的分支；`enumerate` 同时拿下标和值；边加边取余，数值始终小于 `k`（Python 整数本不会溢出，这是惯用做法）。

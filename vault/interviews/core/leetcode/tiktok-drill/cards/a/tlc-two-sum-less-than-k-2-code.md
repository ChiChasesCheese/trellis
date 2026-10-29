---
id: tlc-two-sum-less-than-k-2-code
node: a.two-sum-less-than-k
type: qa
step: 2
---
## Q
**LC 1099 小于 K 的两数之和**｜写出 Python 实现

整数数组 `nums`（长度 `1..100`，元素 `1..1000`）和整数 `k`（`1..2000`）。返回满足 `nums[i] + nums[j] < k`（`i < j`）的最大和，不存在返回 `-1`。不要改动调用者传入的数组。

## A
**思路。** 先得到排序后的新数组，`lo = 0`、`hi = n - 1`。当 `lo < hi`：算和 `s`；`s < k` 就更新最优并 `lo += 1`；否则 `hi -= 1`。循环结束返回 `best`（初值 `-1`）。

```python
def two_sum_less_than_k(nums: list[int], k: int) -> int:
    nums = sorted(nums)                         # 排序后用对撞双指针；sorted 不改动调用者的数组
    lo, hi = 0, len(nums) - 1
    best = -1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s < k:
            best = max(best, s)                 # 合法：记录；lo 与更小的 hi 搭配只会更小，lo 可以排除
            lo += 1
        else:
            hi -= 1                             # 太大：hi 与任何更大的 lo 搭配都太大，hi 可以排除
    return best
```

**运行。** `[34,23,1,24,75,33,54,8]`，`k = 60` → `58`；`[10,20,30]`，`k = 15` → `-1`；`[5]`，`k = 10` → `-1`；`[10,20,30]`，`k = 30` → `-1`；`[1,1]`，`k = 3` → `2`；`[1,1]`，`k = 2` → `-1`。

**复杂度。** 时间 `O(n log n)`：排序 `O(n log n)`，双指针 `O(n)`；空间 `O(n)`（`sorted` 的拷贝）。

**写法要点。** `nums = sorted(nums)` 重新绑定到新列表，不改动调用者的数组（`nums.sort()` 是原地排序且返回 `None`）；`best` 初值 `-1` 正好是「无解」的返回值，不需要额外判断；`max(best, s)` 一行更新，比 `if s > best` 更短；`while lo < hi` 保证 `i < j`，单元素数组直接不进循环。

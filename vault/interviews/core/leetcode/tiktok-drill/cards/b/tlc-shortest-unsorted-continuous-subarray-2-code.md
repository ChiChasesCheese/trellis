---
id: tlc-shortest-unsorted-continuous-subarray-2-code
node: b.shortest-unsorted-continuous-subarray
type: qa
step: 2
---
## Q
**LC 581 最短无序连续子数组**｜写出 Python 实现

整数数组 `nums`（`1 <= nums.length <= 10^4`，`-10^5 <= nums[i] <= 10^5`），求最短的连续子数组，排序它之后整个数组升序；已有序返回 `0`。要求 `O(n)` 时间。

## A
**思路。** 一个循环里从两端同时走：左指针 `i` 向右，维护前缀最大值 `hi`，遇到比 `hi` 小的就把 `end` 推到 `i`；右指针 `j` 向左，维护后缀最小值 `lo`，遇到比 `lo` 大的就把 `start` 推到 `j`。最后长度是 `end - start + 1`。

```python
from math import inf


def find_unsorted_subarray(nums: list[int]) -> int:
    n = len(nums)
    start, end = 0, -1                     # 初始 end - start + 1 == 0，即已有序
    hi, lo = -inf, inf                     # 从左看的最大值；从右看的最小值
    for i in range(n):
        if nums[i] < hi:                   # 左边有更大的数，i 必须被排序
            end = i
        else:
            hi = nums[i]
        j = n - 1 - i
        if nums[j] > lo:                   # 右边有更小的数，j 必须被排序
            start = j
        else:
            lo = nums[j]
    return end - start + 1
```

运行：`[2,6,4,8,10,9,15]` → `5`，`[1,2,3,4]` → `0`，`[1]` → `0`，`[2,1]` → `2`，`[1,1,1]` → `0`，`[1,3,2,2,2]` → `4`，长度 `10^4` 的降序数组 → `10000`。

**复杂度。** 时间 `O(n)`，只扫一遍；空间 `O(1)`，不改入参。

**写法要点。** `from math import inf` 当哨兵，`-inf` 和任意整数比较都成立，不用特判第一个元素；`j = n - 1 - i` 在同一个循环里镜像地从右端走；`else` 分支才更新 `hi` / `lo`，保证它们始终是“已扫描部分的最大 / 最小值”。如果不要求线性，`sorted(nums)` 与原数组 `zip` 比较找第一个、最后一个不同的位置，四行就够。

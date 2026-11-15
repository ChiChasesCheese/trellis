---
slug: points-that-intersect-with-cars
---
## Q
**LC 2848 与车相交的点**｜Easy

`nums[i] = [start, end]` 表示第 `i` 辆车在数轴上占据 `start` 到 `end` 的所有整数点（含端点）。求至少被一辆车覆盖的整数点个数。

## A
**一句话。** 按起点排序，合并区间时只统计新增的点：维护已覆盖到的最右点 `end`，新区间只有超出 `end` 的部分才是新点。

```python
def number_of_points(nums):
    ans = 0
    end = 0                              # 已经统计到的最右点
    for s, e in sorted(nums):
        if e > end:
            ans += e - max(s, end + 1) + 1   # 只加新点
            end = e
    return ans
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`。

**易错点。**
- 区间长度直接相加：重叠部分会重复计数。
- `s` 不和 `end + 1` 取较大值：起点落在已覆盖区间内时，会重复统计。

**追问。**
- 坐标范围很小怎么做？：差分数组，`start +1`、`end + 1` 处 `-1`，再数前缀和大于 `0` 的个数。

**同模式。** LC 253 会议室 II、LC 1109 航班预订统计、LC 56 合并区间

---
slug: find-first-and-last-position-of-element-in-sorted-array
---
## Q
**LC 34 在排序数组中查找元素的第一个和最后一个位置**｜Medium

非递减数组 `nums` 中找 `target` 的起止下标，不存在返回 `[-1, -1]`，要求 `O(log n)`。

## A
**一句话。** 两次二分：第一个 `>= target` 的位置是起点，第一个 `> target` 的位置减一是终点。

```python
def search_range(nums, target):
    lo = bisect_left(nums, target)    # 第一个 >= target
    if lo == len(nums) or nums[lo] != target:
        return [-1, -1]
    hi = bisect_right(nums, target) - 1   # 第一个 > target 前一位
    return [lo, hi]
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 不检查存在性：`[5,7,7,8,8,10]`、`target=6` 会返回 `[1, 0]`，应为 `[-1, -1]`。
- 手写二分用闭区间：答案可能是 `len(nums)`，区间必须左闭右开 `[0, len(nums))`，否则 `([1,3], 3)` 会错。

**追问。**
- 只问出现几次？：`bisect_right - bisect_left`。
- 旋转后的有序数组怎么找（LC 33）？：先判断哪半边有序，再决定往哪边走。

**同模式。** LC 35 搜索插入位置、LC 704 二分查找、LC 162 寻找峰值、LC 153 寻找旋转排序数组中的最小值

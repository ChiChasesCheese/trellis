---
slug: binary-search
---
## Q
**LC 704 二分查找**｜Easy

升序数组 `nums`（元素互不相同）中查找 `target`，返回下标，不存在返回 `-1`。

## A
**一句话。** 左闭右开区间 `[lo, hi)` 找第一个 `>= target` 的位置，最后检查它是否等于 `target`。

```python
def search(nums, target):
    lo, hi = 0, len(nums)        # [lo, hi)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1         # 排除 [lo, mid]
        else:
            hi = mid             # mid 可能是答案
    if lo < len(nums) and nums[lo] == target:
        return lo
    return -1
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 闭区间 `while lo <= hi` 却写 `hi = mid`：区间不收缩，`[5]`、`target=2` 死循环。
- 左闭右开却写 `lo = mid`：`[1,2]`、`target=2` 时死循环。
- 不检查 `lo < len(nums)`：`target` 比所有元素大时 `nums[lo]` 越界。

**追问。**
- 有重复元素，找首个或最后一个位置？：首个是 `bisect_left`，最后一个是 `bisect_right - 1`。
- 答案空间上的二分？：把有序数组换成单调的判定函数，同一模板（LC 875）。

**同模式。** LC 35 搜索插入位置、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 33 搜索旋转排序数组、LC 74 搜索二维矩阵

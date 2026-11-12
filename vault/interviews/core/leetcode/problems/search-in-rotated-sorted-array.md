---
slug: search-in-rotated-sorted-array
---
## Q
**LC 33 搜索旋转排序数组**｜Medium

升序且互不相同的数组被旋转过。在 `O(log n)` 内找 `target` 的下标，不存在返回 `-1`。

## A
**一句话。** 二分，劈开后至少一半有序：判断哪半有序，看 `target` 是否落在它的值域里再决定去向。

```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:       # 左半有序
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                           # 右半有序
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 判有序写成 `nums[lo] < nums[mid]`：区间剩两个元素时误判，`[3,1]`、`target=1` 得 `-1`，应为 `1`。
- 值域比较两端都取闭：`mid` 已查过，左半要写 `target < nums[mid]`。

**追问。**
- 有重复元素（LC 81）？：`nums[lo] == nums[mid] == nums[hi]` 时无法判断，两端各缩一格，最坏 `O(n)`。
- 找旋转数组的最小值（LC 153）？：`nums[mid] > nums[hi]` 往右，否则往左。

**同模式。** LC 81 搜索旋转排序数组 II、LC 153 寻找旋转排序数组中的最小值、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 162 寻找峰值

---
slug: find-minimum-in-rotated-sorted-array
---
## Q
**LC 153 寻找旋转排序数组中的最小值**｜Medium

元素互不相同的升序数组经过旋转，找出最小元素，要求 `O(log n)`。

## A
**一句话。** 二分「断崖」：`nums[mid]` 与右端点比，大于说明最小值在右边，否则在 `[lo, mid]`。

```python
def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:   # 断崖在 mid 右边
            lo = mid + 1
        else:                      # mid 可能就是最小值
            hi = mid
    return nums[lo]
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 和 `nums[lo]` 比较：没旋转时一路右移，`[11,13,15,17]` 返回 `17`，应为 `11`。
- 写 `hi = mid - 1`：跳过恰好是最小值的 `mid`，`[4,5,1,2,3]` 返回 `4`。

**追问。**
- 有重复元素（LC 154）？：`nums[mid] == nums[hi]` 时只能 `hi -= 1`，最坏 `O(n)`。
- 在旋转数组里找目标（LC 33）？：先判断 `mid` 落在哪一段，再看目标是否在有序那段里。

**同模式。** LC 154 寻找旋转排序数组中的最小值 II、LC 33 搜索旋转排序数组、LC 162 寻找峰值、LC 852 山脉数组的峰顶索引

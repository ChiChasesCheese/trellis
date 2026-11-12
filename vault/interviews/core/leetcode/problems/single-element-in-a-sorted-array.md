---
slug: single-element-in-a-sorted-array
---
## Q
**LC 540 有序数组中的单一元素**｜Medium

有序数组中每个数出现两次，只有一个数出现一次，找出它，要求 `O(log n)`、`O(1)`。

## A
**一句话。** 二分下标奇偶性：单一元素前每对从偶数下标开始，其后从奇数下标开始。

```python
def single_non_duplicate(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        mid -= mid & 1           # 对齐到偶数下标
        if nums[mid] == nums[mid + 1]:
            lo = mid + 2         # 这对完整，单一元素在右边
        else:
            hi = mid
    return nums[lo]
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 不对齐 `mid`：奇数 `mid` 是一对的右端，判断含义变了，`[3,3,7,7,10,11,11]` 得 `7`，应为 `10`。
- 写 `lo = mid + 1`：破坏 `lo` 的偶数性，一对有两个元素要跳 `2`。
- 用 `lo <= hi` 配 `hi = mid`：`lo == hi` 时死循环。

**追问。**
- 数组无序（LC 136）？：全体异或，`O(n)`、`O(1)`。
- 其余数都出现三次（LC 137）？：异或失效，按位统计 `1` 的个数模 `3`。

**同模式。** LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 162 寻找峰值、LC 153 寻找旋转排序数组中的最小值、LC 136 只出现一次的数字

---
slug: find-minimum-in-rotated-sorted-array-ii
---
## Q
**LC 154 寻找旋转排序数组中的最小值 II**｜Hard

升序数组（可含重复）被旋转后得到 `nums`，求其中的最小元素。

## A
**一句话。** 二分比较 `nums[mid]` 与右端点：更大则最小值在右边，更小则在 `mid` 或左边，相等就丢掉右端点。

```python
def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1     # 最小值在 mid 右边
        elif nums[mid] < nums[hi]:
            hi = mid         # 在 mid 或左边
        else:
            hi -= 1          # 相等：nums[mid] 是替身，可丢 hi
    return nums[lo]
```

**复杂度。** 时间 平均 `O(log n)`、最坏 `O(n)`，空间 `O(1)`。

**易错点。**
- 相等时写 `hi = mid`：`[3,3,1,3]` 得 `3`，应为 `1`，最小值可能在 `mid` 右边。
- 相等时 `lo += 1`：`[1,3,3]` 得 `3`，应为 `1`，丢掉的左端点可能正是最小值。
- 拿 `nums[mid]` 和左端点比较：数组已有序时失效，`[1,3,5]` 得 `5`。

**追问。**
- 为什么重复让最坏变成 `O(n)`？：`[1,1,1,0,1,1]` 里的 `0` 可以在任意位置，不查完其他位置无法确定。
- 无重复版本（LC 153）？：去掉相等分支，严格 `O(log n)`。

**同模式。** LC 153 寻找旋转排序数组中的最小值、LC 33 搜索旋转排序数组、LC 81 搜索旋转排序数组 II、LC 162 寻找峰值

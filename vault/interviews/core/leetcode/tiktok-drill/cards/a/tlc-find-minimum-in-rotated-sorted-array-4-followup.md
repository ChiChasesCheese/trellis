---
id: tlc-find-minimum-in-rotated-sorted-array-4-followup
node: a.find-minimum-in-rotated-sorted-array
type: qa
step: 4
---
## Q
**LC 153 寻找旋转排序数组中的最小值**｜追问

面试官接着问：（1）数组里有重复元素怎么办，复杂度会变吗？（2）要在旋转数组里搜索某个目标值，怎么改？（3）只问被旋转了多少次？

## A
1. **有重复（LC 154）**：多出一种情况 `nums[mid] == nums[hi]`，此时最小值可能在左也可能在右，无法判断。安全做法是 `hi -= 1`（丢掉一个相等的右端点，最小值不会丢，因为还有同值的 `mid`）。
```python
def find_min_dup(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        elif nums[mid] < nums[hi]:
            hi = mid
        else:
            hi -= 1
    return nums[lo]
```
`[2,2,2,0,1]` → `0`，`[1,1,1]` → `1`。全相同时每轮只缩一格，最坏 `O(n)`，平均仍接近 `O(log n)`。这是重复元素让二分失去判断依据的根本原因。
2. **搜索目标（LC 33）**：每轮先看 `[lo, mid]` 和 `[mid, hi]` 哪一段有序，再看目标是否落在有序段的值域内，落在就收缩到那段，否则去另一段，仍是 `O(log n)`。
3. **旋转次数**：就是最小值的下标 `lo`（原数组恰好没旋转时为 `0`）。

**Python 提醒**：`bisect_left(a, x, key=...)` 的 `key` 只作用于 `a` 的元素、不作用于 `x`，所以传入 `range(n)` 加 `key=lambda i: ...` 时，`x` 要写成已经变换后的值（这里是 `True`）。

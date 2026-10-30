---
id: tlc-search-in-rotated-sorted-array-4-followup
node: p2.search-in-rotated-sorted-array
type: qa
step: 4
---
## Q
**LC 33 搜索旋转排序数组**｜追问

面试官接着问：（1）数组里有重复元素（LC 81）怎么改？最坏复杂度是多少？（2）只要找旋转后数组的最小值（LC 153）？（3）能不能用 `bisect` 把二分写得更短？

## A
1. **有重复元素**：问题出在 `nums[lo] == nums[mid] == nums[hi]` 时，无法判断哪半有序（如 `[1,0,1,1,1]`）。这时只能把两端各缩一格，其余逻辑不变。最坏情况（全是相同值）退化成 `O(n)`。

```python
def search_dup(nums: list[int], target: int) -> bool:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return True
        if nums[lo] == nums[mid] == nums[hi]:
            lo += 1                                  # 看不出哪半有序，只能两端各缩一格
            hi -= 1
        elif nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False
```

`search_dup([2,5,6,0,0,1,2], 0)` → `True`，`search_dup([2,5,6,0,0,1,2], 3)` → `False`，`search_dup([1,0,1,1,1], 0)` → `True`。
2. **找最小值**：比较 `nums[mid]` 与 `nums[hi]`。`nums[mid] > nums[hi]` 说明最小值在右半（排除 `mid`）；否则在 `[lo, mid]`。

```python
def find_min(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]
```
3. **用 `bisect` 的 `key`**（Python 3.10+）：先找旋转点，再在"虚拟有序数组"上二分，不用自己判断哪半有序。

```python
from bisect import bisect_left


def search_bisect(nums: list[int], target: int) -> int:
    n = len(nums)
    k = bisect_left(range(n), True, key=lambda i: nums[i] < nums[0]) % n     # 旋转点，没旋转时为 0
    i = bisect_left(range(n), target, key=lambda i: nums[(i + k) % n])       # 在"虚拟有序数组"上二分
    return (i + k) % n if i < n and nums[(i + k) % n] == target else -1
```

`search_bisect([4,5,6,7,0,1,2], 0)` → `4`，`search_bisect([1], 0)` → `-1`。

**Python 提醒**：`key` 只作用在序列元素上，第二个参数 `x` 不会被 `key` 变换；`key` 的结果必须单调。

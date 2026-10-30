---
id: tlc-find-first-and-last-position-of-element-in-sorted-array-2-code
node: p3.find-first-and-last-position-of-element-in-sorted-array
type: qa
step: 2
---
## Q
**LC 34 在排序数组中查找元素的第一个和最后一个位置**｜写出 Python 实现

非递减整数数组 `nums`（长度 `0` 到 `10^5`，元素和 `target` 都在 `[-10^9, 10^9]`），返回 `target` 第一次和最后一次出现的下标，不存在返回 `[-1, -1]`。要求 `O(log n)`。

## A
**思路。** `bisect_left` 给出第一个 `>= target` 的位置 `lo`；它越界或值不等于 `target` 就不存在。`bisect_right` 给出第一个 `> target` 的位置，减一是最后一个。

```python
from bisect import bisect_left, bisect_right

def search_range(nums: list[int], target: int) -> list[int]:
    lo = bisect_left(nums, target)          # 第一个 >= target 的位置
    if lo == len(nums) or nums[lo] != target:
        return [-1, -1]                     # 越界或该位置不是 target：不存在
    hi = bisect_right(nums, target) - 1     # 第一个 > target 的位置再减 1 = 最后一个 target
    return [lo, hi]
```

运行：`([5,7,7,8,8,10], 8)` → `[3, 4]`，`([5,7,7,8,8,10], 6)` → `[-1, -1]`，`([], 0)` → `[-1, -1]`，`([1], 1)` → `[0, 0]`，`([2,2], 2)` → `[0, 1]`，`([1,3], 4)` → `[-1, -1]`。

**复杂度。** 时间 `O(log n)`：两次二分各约 `log2(10^5) ≈ 17` 步；空间 `O(1)`。

**写法要点。**
- `bisect_left` 返回「第一个 `>= x` 的插入点」，`bisect_right`（即 `bisect`）返回「第一个 `> x` 的插入点」，相同元素排在它们之间。
- 先判断 `lo == len(nums)` 再取 `nums[lo]`：短路求值避免下标越界。
- 手写版本要用左闭右开 `[0, len(nums))`：`while lo < hi`，`nums[mid] < x` 时 `lo = mid + 1`，否则 `hi = mid`；结束时 `lo` 就是下界，可能等于 `len(nums)`。
- Python 3.10 起 `bisect` 支持 `key=` 参数（对元素取键，`x` 本身不经过 `key`），可直接在元组列表上二分。

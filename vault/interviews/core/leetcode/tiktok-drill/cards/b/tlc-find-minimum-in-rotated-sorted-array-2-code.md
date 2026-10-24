---
id: tlc-find-minimum-in-rotated-sorted-array-2-code
node: b.find-minimum-in-rotated-sorted-array
type: qa
step: 2
---
## Q
**LC 153 寻找旋转排序数组中的最小值**｜写出 Python 实现

`nums` 由元素互不相同的升序数组旋转而来（`1 <= n <= 5000`，值在 `[-5000, 5000]`），返回其中的最小值，要求 `O(log n)`。

## A
**思路。** 区间 `[lo, hi]` 里一直包含最小值。取中点，与右端点比较：中点比右端点大，说明断崖在中点右边，丢掉 `[lo, mid]`；否则中点已经在右半段，最小值在 `[lo, mid]`，丢掉 `(mid, hi]`。区间缩成一个元素时返回它。

```python
def find_min(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:                      # 区间收缩到一个元素时，它就是最小值
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:        # 断崖在 mid 右边，最小值在 (mid, hi]
            lo = mid + 1
        else:                           # mid 已在右半段，最小值在 [lo, mid]
            hi = mid
    return nums[lo]
```

库函数写法（Python 3.10+ 的 `bisect` 支持 `key`）：

```python
from bisect import bisect_left

def find_min_bisect(nums: list[int]) -> int:
    # 谓词「nums[i] <= nums[-1]」在左半段全 False、右半段全 True，是单调的
    return nums[bisect_left(range(len(nums)), True, key=lambda i: nums[i] <= nums[-1])]
```

运行：`[3,4,5,1,2]` → `1`，`[4,5,6,7,0,1,2]` → `0`，`[11,13,15,17]` → `11`，`[1]` → `1`，`[2,1]` → `1`；两种写法结果一致。

**复杂度。** 时间 `O(log n)`；空间 `O(1)`（`range` 是惰性对象，不展开成列表）。

**写法要点。** 循环条件 `lo < hi` 配 `hi = mid`，保证区间每轮严格缩小；`bisect_left(range(n), True, key=...)` 对下标做二分，`key` 把下标映射成布尔，`False < True` 所以谓词必须是「先假后真」；不用 `(lo + hi) >> 1` 这类技巧，Python 整数不会溢出。

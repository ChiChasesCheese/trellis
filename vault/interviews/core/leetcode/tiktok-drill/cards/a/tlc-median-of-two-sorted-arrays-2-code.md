---
id: tlc-median-of-two-sorted-arrays-2-code
node: a.median-of-two-sorted-arrays
type: qa
step: 2
---
## Q
**LC 4 寻找两个正序数组的中位数**｜写出 Python 实现

两个升序数组 `nums1`、`nums2`（长度 `m`、`n`，`0 <= m, n <= 1000`，`1 <= m + n <= 2000`，值在 `[-10^6, 10^6]`）。返回合并后的中位数（浮点数），要求时间 `O(log(m + n))`。

## A
**思路。** 保证 `a` 是较短的数组，对 `a` 取前 `i` 个元素二分；`b` 取前 `j = half - i` 个，`half = (m + n + 1) // 2`。检查切口两侧：`a_left > b_right` 说明 `i` 太大，`b_left > a_right` 说明 `i` 太小，否则切法合法。合法时，左半最大值是 `max(a_left, b_left)`；总数为奇数时它就是答案，偶数时再和右半最小值取平均。

```python
from math import inf


def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    a, b = (nums1, nums2) if len(nums1) <= len(nums2) else (nums2, nums1)   # 在较短的数组上二分
    m, n = len(a), len(b)
    half = (m + n + 1) // 2             # 左半边的元素个数（总数为奇数时，左边多一个）
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2              # a 的前 i 个进左半边
        j = half - i                    # b 的前 j 个进左半边
        a_left = a[i - 1] if i > 0 else -inf
        a_right = a[i] if i < m else inf
        b_left = b[j - 1] if j > 0 else -inf
        b_right = b[j] if j < n else inf
        if a_left > b_right:            # a 取多了：左边界往左挪
            hi = i - 1
        elif b_left > a_right:          # a 取少了：往右挪
            lo = i + 1
        else:                           # 左半边每个数都 <= 右半边每个数
            left_max = max(a_left, b_left)
            if (m + n) % 2:
                return float(left_max)
            return (left_max + min(a_right, b_right)) / 2
    raise ValueError("输入不是有序数组")
```

运行：`([1,3], [2])` → `2.0`，`([1,2], [3,4])` → `2.5`，`([], [1])` → `1.0`，`([2], [])` → `2.0`，`([0,0], [0,0])` → `0.0`，`([1,2,3,4,5], [6])` → `3.5`。

**复杂度。** 时间 `O(log min(m, n))`：每轮把 `a` 上的搜索区间减半；空间 `O(1)`。

**写法要点。** `math.inf` 当哨兵，和整数可以直接比较，省掉四处 `if i == 0` 的特判；`a, b = (nums1, nums2) if ... else (nums2, nums1)` 一行把较短的放在 `a`；`half = (m + n + 1) // 2` 对奇数和偶数统一处理：奇数时左半多一个，中位数就是左半最大值；偶数时左右等长；`float(left_max)` 把整数转成浮点，返回类型统一；循环末尾的 `raise` 只在输入不是有序数组时才会到达，让函数的所有路径都有明确的结果。

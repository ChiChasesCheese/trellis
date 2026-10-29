---
id: tlc-sliding-window-median-5-alt
node: a.sliding-window-median
type: qa
step: 5
---
## Q
**LC 480 滑动窗口中位数**｜另一种解法

不用对顶堆，只用标准库的 `bisect` 维护一个有序窗口怎么写？复杂度如何，什么时候可以接受？

## A
**思路。** 窗口始终保持为有序列表：读中位数直接按下标取；滑出时 `bisect_left` 找到该值的位置删掉，滑入时 `insort` 插到正确位置。

```python
from bisect import bisect_left, insort


def median_sliding_window_sorted(nums: list[int], k: int) -> list[float]:
    window = sorted(nums[:k])
    res: list[float] = []
    for i in range(k, len(nums) + 1):
        res.append(float(window[k // 2]) if k % 2 else (window[k // 2 - 1] + window[k // 2]) / 2)
        if i == len(nums):
            break
        window.pop(bisect_left(window, nums[i - k]))   # 二分找到滑出的元素，删除是 O(k) 搬移
        insort(window, nums[i])                         # 二分找插入位置，插入也是 O(k)
    return res
```

运行：`[1,3,-1,-3,5,3,6,7], k=3` → `[1.0, -1.0, -1.0, 3.0, 5.0, 6.0]`，`[1,4,2,3], k=4` → `[2.5]`。

**复杂度。** 查找 `O(log k)`，但列表中间插入和删除要搬移 `O(k)` 个元素，总时间 `O(nk)`，空间 `O(k)`。

**取舍。** 搬移是 C 层的整段内存移动，常数很小，`k` 不大或 `n·k` 在 `10^8` 量级以内时实际很快，而且几乎不会写错，适合先给出正确解。`k` 接近 `n / 2` 时 `n·k` 达到 `10^9` 级，最坏情况落后对顶堆一个数量级；对顶堆每步 `O(log n)`，是面试官期待的最优解，但不变量多、易出错。先说清两者的复杂度，再写对顶堆。

---
id: tlc-median-of-two-sorted-arrays-4-followup
node: p3.median-of-two-sorted-arrays
type: qa
step: 4
---
## Q
**LC 4 寻找两个正序数组的中位数**｜追问

面试官接着问：（1）能不能二分**值域**而不是切割点？（2）数组是**数据流**，不断有新元素加入，怎么随时给出中位数？（3）有 `k` 个有序数组呢？

## A
1. **二分值**：中位数是第 `k` 小。对候选值 `x`，用 `bisect_right` 统计两个数组中 `<= x` 的元素个数 `cnt(x)`；`cnt(x) >= k` 的最小 `x` 就是第 `k` 小。值域 `[-10^6, 10^6]`，约 `21` 轮，每轮两次 `bisect`，总共 `O(log V · log(m + n))`，代码短，不容易出错，但不依赖数组长度。

```python
from bisect import bisect_right


def kth_by_value(a: list[int], b: list[int], k: int) -> int:
    lo, hi = -10**6, 10**6
    while lo < hi:
        mid = (lo + hi) // 2
        if bisect_right(a, mid) + bisect_right(b, mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

2. **数据流中位数（LC 295）**：一个大顶堆装较小的一半，一个小顶堆装较大的一半，保持两堆大小相差不超过 `1`。每次加入 `O(log n)`，取中位数 `O(1)`。Python 的 `heapq` 只有小顶堆，大顶堆存负数。
3. **`k` 个有序数组**：切割法推广到 `k` 个数组比较麻烦；常用做法是二分值域加 `k` 次 `bisect`，`O(k log V log n)`；或者用堆做 `k` 路归并，走到中间位置，`O(n log k)`（`n` 为总元素数）。

**Python 提醒**：`float(x)` 与 `x / 2` 的返回类型要统一成浮点；`statistics.median` 对奇数个整数返回整数，对偶数个返回浮点，不能直接当作返回 `float` 的函数用。`math.inf` 可以和整数比较，也可以参与 `max` / `min`，但 `inf - inf` 是 `nan`，不要在哨兵之间做减法。

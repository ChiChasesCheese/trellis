---
id: tlc-subarray-with-elements-greater-than-varying-threshold-4-followup
node: a.subarray-with-elements-greater-than-varying-threshold
type: qa
step: 4
---
## Q
**LC 2334 元素值大于变化阈值的子数组**｜追问

面试官接着问：（1）要返回**最大**的合法长度？（2）这题和「柱状图中最大的矩形」（LC 84）是什么关系？（3）为什么不能用固定大小的滑动窗口？

## A
1. **最大合法长度**：不再遇到第一个就返回，而是对所有满足 `h * k > threshold` 的 `k` 取最大。合法子数组的最大长度一定出现在某个元素的最宽区间上（见正确性的论证）。

```python
from itertools import chain


def largest_valid_size(nums: list[int], threshold: int) -> int:
    stack: list[int] = []
    best = -1
    for i, x in enumerate(chain(nums, (0,))):
        while stack and nums[stack[-1]] >= x:
            h = nums[stack.pop()]
            left = stack[-1] if stack else -1
            k = i - left - 1
            if h * k > threshold:
                best = max(best, k)
        stack.append(i)
    return best
```

`largest_valid_size([6,5,6,5,8], 7)` → `5`，`largest_valid_size([1,3,4,3,1], 6)` → `3`。
2. **与 LC 84 的关系**：LC 84 求 `max(h * k)`，即以每个元素为最小值的最大矩形面积；这里只问是否存在 `h * k > threshold`。栈的结构完全一样，LC 84 取最大面积，LC 2334 提前返回或取最大宽度。如果题目改成"求最大的 `m * k`，看它是否超过阈值"，直接复用 LC 84 的代码。
3. **固定窗口行不通**：每个长度 `k` 的阈值 `threshold / k` 都不同，要对每个 `k` 各做一次"滑动窗口最小值"，总计 `O(n^2)`。只有把"以谁为最小值"当作枚举对象，才能把所有 `k` 一次处理完。

**Python 提醒**：要同时拿到每个元素左右两边第一个更小元素的位置，一遍栈扫描就够；不要写成对每个元素向两边各扫一次，最坏 `O(n^2)`。比较大数乘积时 Python 不会溢出，但换成 C++ / Java 需要 64 位整数。

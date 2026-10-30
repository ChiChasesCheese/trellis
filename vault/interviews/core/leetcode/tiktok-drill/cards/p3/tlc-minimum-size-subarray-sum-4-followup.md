---
id: tlc-minimum-size-subarray-sum-4-followup
node: p3.minimum-size-subarray-sum
type: qa
step: 4
---
## Q
**LC 209 长度最小的子数组**｜追问

面试官接着问：（1）做出 `O(n)` 之后，再写一个 `O(n log n)` 的解法？（2）要返回子数组本身（或起点终点）？（3）元素允许是负数怎么办？

## A
1. **前缀和加二分。** 元素为正，前缀和 `pre` 严格递增，可以二分：
```python
from bisect import bisect_left
from itertools import accumulate

def min_sub_array_len_bisect(target: int, nums: list[int]) -> int:
    pre = list(accumulate(nums, initial=0))        # pre[i] = nums[:i] 的和；元素为正，所以严格递增
    best = len(nums) + 1
    for i in range(len(nums)):
        j = bisect_left(pre, pre[i] + target)      # 最小的 j 使 pre[j] - pre[i] >= target
        if j <= len(nums):
            best = min(best, j - i)
    return best if best <= len(nums) else 0
```
`(7, [2,3,1,2,4,3])` → `2`。时间 `O(n log n)`，空间 `O(n)`。比滑动窗口慢，但在前缀和已经备好、要回答多个不同 `target` 的场景下很划算。
2. **返回子数组。** 更新答案时记下起点：`if right - left + 1 < best: best, start = right - left + 1, left`，最后返回 `nums[start:start + best]`。`(7, [2,3,1,2,4,3])` 得到 `[4, 3]`。
3. **含负数。** 前缀和不再单调，二分和滑动窗口都失效。用单调递增的双端队列存前缀和的下标：右端到来时，从队首弹出所有满足 `pre[r] - pre[队首] >= target` 的起点并更新答案，再从队尾弹掉前缀和不小于当前的下标。每个下标进出各一次，`O(n)`（LC 862）。

**Python 提醒**：`itertools.accumulate(nums, initial=0)` 会在前面补一个 `0`，比 `[0, *accumulate(nums)]` 更直接；`bisect_left` 作用在列表上，列表必须有序，含负数时前缀和无序，结果不可靠。

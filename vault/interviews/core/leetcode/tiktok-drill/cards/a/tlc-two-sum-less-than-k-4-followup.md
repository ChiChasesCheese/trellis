---
id: tlc-two-sum-less-than-k-4-followup
node: a.two-sum-less-than-k
type: qa
step: 4
---
## Q
**LC 1099 小于 K 的两数之和**｜追问

面试官接着问：（1）怎么统计和小于 `k` 的数对有多少对？（2）不用双指针，用二分怎么写？（3）要返回具体的两个数？

## A
1. **统计个数。** `nums[lo] + nums[hi] < k` 时，`lo` 与 `lo + 1` 到 `hi` 的每个数配对都合法（这些数都不超过 `nums[hi]`），一次性加 `hi - lo` 对，然后 `lo += 1`（`lo` 的配对已算完）；否则 `hi -= 1`。这是 LC 259 的写法，排序后扫描 `O(n)`。
2. **二分。** 排序后对每个 `x = nums[i]`，只在它前面的部分里找搭档，用 `bisect_left` 找到第一个 `>= k - x` 的位置，它前一个就是 `< k - x` 的最大数：

```python
from bisect import bisect_left


def two_sum_less_than_k_bisect(nums: list[int], k: int) -> int:
    nums = sorted(nums)
    best = -1
    for i, x in enumerate(nums):
        j = bisect_left(nums, k - x, 0, i)      # 只在 nums[:i] 里找，保证 j < i
        if j:                                   # j 个数严格小于 k - x
            best = max(best, x + nums[j - 1])   # nums[j - 1] 是其中最大的
    return best
```

3. **返回数对。** 更新 `best` 时同时记录 `(nums[lo], nums[hi])`；要原数组下标就先对下标排序：`order = sorted(range(n), key=nums.__getitem__)`。

**Python 提醒**：`bisect_left(a, x, lo, hi)` 的 `hi` 是开区间右端，传 `i` 表示只看 `a[:i]`；`n <= 100` 时暴力 `max((a + b for a, b in combinations(nums, 2) if a + b < k), default=-1)` 也能过，注意要写 `default=-1`，否则没有合法数对时 `max` 抛 `ValueError`。

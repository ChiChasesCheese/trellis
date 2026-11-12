---
slug: frequency-of-the-most-frequent-element
---
## Q
**LC 1838 最高频元素的频数**｜Medium

每步可把一个元素加 `1`，最多 `k` 步，求某个值能达到的最大出现次数。

## A
**一句话。** 排序后滑动窗口：把窗口抬到 `nums[right]` 的代价是 `x·长度 - 窗口和`，超过 `k` 就缩左端。

```python
def max_frequency(nums, k):
    nums.sort()
    left = window = 0
    best = 1
    for r, x in enumerate(nums):
        window += x
        while x * (r - left + 1) - window > k:
            window -= nums[left]
            left += 1
        best = max(best, r - left + 1)
    return best
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`。

**易错点。**
- 不排序：`[3,9,6]`、`k=2` 得 `2`，应为 `1`。
- 缩左端时忘了 `window -= nums[left]`：窗口和偏大，代价被低估，`[1,3,5]`、`k=1` 得 `2`，应为 `1`。

**追问。**
- 为什么窗口不用每次都缩到合法？：答案只增不减，窗口大小只会保持或变大，也可用 `if` 代替 `while`。
- 能二分吗？：能，对每个右端用前缀和二分最左的合法左端，`O(n log n)`。

**同模式。** LC 1004 最大连续 1 的个数 III、LC 424 替换后的最长重复字符、LC 209 长度最小的子数组、LC 2090 半径为 k 的子数组平均值

---
slug: longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit
---
## Q
**LC 1438 绝对差不超过限制的最长连续子数组**｜Medium

求最长子数组的长度，要求其中任意两个元素之差的绝对值都不超过 `limit`。

## A
**一句话。** 滑动窗口加两个单调队列，维护窗口最大、最小值，`max - min > limit` 时收缩左端。

```python
def longest_subarray(nums, limit):
    mx, mn = deque(), deque()   # 递减 / 递增，队首是最大 / 最小
    left = best = 0
    for r, x in enumerate(nums):
        while mx and mx[-1] < x:
            mx.pop()
        mx.append(x)
        while mn and mn[-1] > x:
            mn.pop()
        mn.append(x)
        while mx[0] - mn[0] > limit:
            if mx[0] == nums[left]:
                mx.popleft()
            if mn[0] == nums[left]:
                mn.popleft()
            left += 1
        best = max(best, r - left + 1)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 弹出时用 `<=` / `>=`：相等元素被弹掉，左端按值移除会误删，队列变空后 `IndexError`（`[3,3,1,3]`、`limit = 0`）。
- 只比较相邻元素：`[8,2,4,7]`、`limit = 4` 会得 `3`，但 `7 - 2 = 5`，应为 `2`。

**追问。**
- 为什么两个单调队列就够？：任意两数之差最大的一对必是窗口的最大与最小。
- 能用有序容器代替吗？：可以，但增删 `O(log n)`，总 `O(n log n)`。

**同模式。** LC 239 滑动窗口最大值、LC 3 无重复字符的最长子串、LC 862 和至少为 K 的最短子数组

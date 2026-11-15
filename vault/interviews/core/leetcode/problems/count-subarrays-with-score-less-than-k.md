---
slug: count-subarrays-with-score-less-than-k
---
## Q
**LC 2302 统计得分小于 K 的子数组数目**｜Hard

正整数数组 `nums`，子数组的分数 = 元素和 × 长度。求分数严格小于 `k` 的非空子数组个数。

## A
**一句话。** 元素全正，分数随窗口变长而单调变大，用不定长滑窗：右端每进一格就收缩到合法，再加上以右端结尾的 `right-left+1` 个子数组。

```python
def count_subarrays(nums, k):
    ans = s = left = 0
    for right, x in enumerate(nums):
        s += x
        # 分数 >= k 就缩左端，直到窗口合法
        while s * (right - left + 1) >= k:
            s -= nums[left]
            left += 1
        ans += right - left + 1   # 以 right 结尾的都合法
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 收缩条件写成 `>`：分数等于 `k` 也不合法，要用 `>=`。
- 每步只加 `1`：合法窗口内以 `right` 结尾的子数组有 `right-left+1` 个。

**追问。**
- 为什么能用滑窗？：全是正数，大窗口不合法则包含它的更大窗口也不合法，左端只会右移。
- 元素可以为负？：单调性没了，滑窗失效，要换前缀和加数据结构。

**同模式。** LC 209 长度最小的子数组、LC 713 乘积小于 K 的子数组、LC 2762 不间断子数组

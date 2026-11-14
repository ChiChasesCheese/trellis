---
slug: length-of-longest-subarray-with-at-most-k-frequency
---
## Q
**LC 2958 最多 K 个重复元素的最长子数组**｜Medium

求最长子数组，使其中每个元素出现次数都不超过 `k`。

## A
**一句话。** 不定长滑动窗口：右端加入 `x` 后只有 `x` 可能超标，就一直移左端直到 `x` 的次数回到 `k`。

```python
def max_subarray_length(nums, k):
    cnt = Counter()
    left = ans = 0
    for right, x in enumerate(nums):
        cnt[x] += 1
        while cnt[x] > k:        # 只有刚加入的 x 会超标
            cnt[nums[left]] -= 1
            left += 1
        ans = max(ans, right - left + 1)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 收缩条件检查整个窗口：没必要，其他元素次数这一步没变。
- 在 `while` 里更新答案：要等窗口合法后再更新。

**追问。**
- 改成「至少有一个元素出现 `≥ k` 次」计数（LC 2962 类）？：越长越合法，统计左端点个数。
- 为什么左端点只右移？：窗口变短只会让次数变小，合法窗口的子窗口也合法。

**同模式。** LC 3 无重复字符的最长子串、LC 3090 每个字符最多出现两次的最长子字符串、LC 1004 最大连续1的个数 III

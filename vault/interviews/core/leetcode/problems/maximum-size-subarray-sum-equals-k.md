---
slug: maximum-size-subarray-sum-equals-k
---
## Q
**LC 325 和等于 k 的最长子数组长度**｜Medium

数组 `nums` 与目标 `k`，求和等于 `k` 的最长连续子数组的长度，没有返回 `0`。

## A
**一句话。** 前缀和加哈希表，只记每个前缀和第一次出现的下标，查 `前缀和 - k`。

```python
def max_sub_array_len(nums, k):
    first = {0: -1}       # 前缀和 -> 最早下标；空前缀在 -1
    prefix = best = 0
    for i, x in enumerate(nums):
        prefix += x
        if prefix - k in first:
            best = max(best, i - first[prefix - k])
        first.setdefault(prefix, i)   # 只记第一次，保证最长
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用 `first[prefix] = i` 覆盖：记成最近位置会得到最短子数组，`[0,0,0]`、`k=0` 得 `1` 而不是 `3`。
- 忘了 `{0: -1}`：从开头就满足的子数组算不出，`[1,-1,5,-2,3]`、`k=3` 得 `2`。

**追问。**
- 为什么不能用滑动窗口？：有负数，窗口和不单调。
- 求最短的呢？：哈希表改存最近出现的位置。

**同模式。** LC 560 和为 K 的子数组、LC 525 连续数组、LC 523 连续的子数组和、LC 974 和可被 K 整除的子数组

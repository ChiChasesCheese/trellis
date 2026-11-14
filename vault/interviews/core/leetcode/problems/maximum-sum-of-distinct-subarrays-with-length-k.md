---
slug: maximum-sum-of-distinct-subarrays-with-length-k
---
## Q
**LC 2461 长度为 K 子数组中的最大和**｜Medium

在所有长度为 `k` 且元素互不相同的子数组中求最大和，没有则返回 `0`。

## A
**一句话。** 定长滑窗：和增量更新，`Counter` 记次数，窗口内不同值的个数等于 `k` 才算合法。

```python
def maximum_subarray_sum(nums, k):
    cnt = Counter()
    s = ans = 0
    for i, x in enumerate(nums):
        cnt[x] += 1                  # 入
        s += x
        if i < k - 1:
            continue
        if len(cnt) == k:            # 窗口内互不相同
            ans = max(ans, s)
        out = nums[i - k + 1]        # 出
        s -= out
        cnt[out] -= 1
        if cnt[out] == 0:
            del cnt[out]
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(k)`。

**易错点。**
- 计数减到 `0` 不删键：`len(cnt)` 会把已滑出的值也算上。
- 每个窗口 `len(set(...))`：`O(nk)`。

**追问。**
- 至少有 `m` 个不同元素（LC 2841）？：条件换成 `len(cnt) >= m`。
- 不定长、元素互不相同的最大和？：不定长滑窗，重复时收缩左端，即 LC 1695。

**同模式。** LC 438 找到字符串中所有字母异位词、LC 643 子数组最大平均数 I、LC 2841 几乎唯一子数组的最大和

---
slug: subarrays-with-k-different-integers
---
## Q
**LC 992 K 个不同整数的子数组**｜Hard

求 `nums` 中恰好含 `k` 个不同整数的子数组个数。

## A
**一句话。** 「恰好 `k`」没有单调性，「至多 `k`」有，所以答案是 `atMost(k) - atMost(k - 1)`。

```python
def subarrays_with_k_distinct(nums, k):
    def at_most(limit):
        cnt = defaultdict(int)
        distinct = left = total = 0
        for r, x in enumerate(nums):
            if cnt[x] == 0:
                distinct += 1
            cnt[x] += 1
            while distinct > limit:     # 超限：收缩左端
                cnt[nums[left]] -= 1
                if cnt[nums[left]] == 0:
                    distinct -= 1
                left += 1
            total += r - left + 1       # 以 r 结尾的合法子数组数
        return total
    return at_most(k) - at_most(k - 1)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 直接对「恰好 `k`」收缩窗口：缩左端后不同数可能仍是 `k` 也可能变 `k-1`，没有单调性，会漏子数组。
- 每步只加 `1`：应加以 `r` 结尾的全部合法左端数 `r - left + 1`。

**追问。**
- 还有哪些题是「恰好 = 至多之差」？：LC 1248 统计优美子数组、LC 930 和相同的二元子数组。
- 只求最长的恰好 `k` 个不同的子数组？：直接滑窗，求最长时单调性够用（LC 340）。

**同模式。** LC 340 至多包含 K 个不同字符的最长子串、LC 904 水果成篮、LC 930 和相同的二元子数组、LC 1248 统计优美子数组

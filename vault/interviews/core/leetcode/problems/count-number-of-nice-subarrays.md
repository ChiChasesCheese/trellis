---
slug: count-number-of-nice-subarrays
---
## Q
**LC 1248 统计「优美子数组」**｜Medium

数出恰好含 `k` 个奇数的连续子数组的个数。

## A
**一句话。** 前缀和计数：前缀里的奇数个数为 `odd`，累加之前出现过的 `odd - k` 的次数。

```python
def number_of_subarrays(nums, k):
    seen = [0] * (len(nums) + 1)   # seen[j]：奇数个数为 j 的前缀数
    seen[0] = 1                    # 空前缀
    odd = ans = 0
    for x in nums:
        odd += x & 1
        if odd >= k:
            ans += seen[odd - k]
        seen[odd] += 1
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 漏掉 `seen[0] = 1`：从开头开始的子数组不计，`[1,1,2,1,1]`、`k=3` 得 `1`，应为 `2`。
- 窗口里每个右端只加 `1`：左端有多个合法起点，`[2,2,2,1,2,2,1,2,2,2]`、`k=2` 得 `4`，应为 `16`。

**追问。**
- 为什么能用数组而不是字典？：奇数个数范围是 `0..n`，直接当下标。
- 滑动窗口怎么做？：`atMost(k) - atMost(k-1)`，每个都是一遍窗口。

**同模式。** LC 560 和为 K 的子数组、LC 930 和相同的二元子数组、LC 974 和可被 K 整除的子数组、LC 992 K 个不同整数的子数组

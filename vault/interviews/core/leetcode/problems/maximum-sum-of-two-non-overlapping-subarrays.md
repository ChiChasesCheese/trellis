---
slug: maximum-sum-of-two-non-overlapping-subarrays
---
## Q
**LC 1031 两个无重叠子数组的最大和**｜Medium

整数数组 `nums`，求长度分别为 `firstLen`、`secondLen` 的两个不重叠子数组的元素和的最大值（两段谁在前都可以）。

## A
**一句话。** 前缀和 + 一遍扫描：固定 `b` 段结束在 `j`，`a` 段只能在 `b` 段之前，用到目前为止最大的 `a` 段和；两个顺序各算一次取大。

```python
def max_sum_two_no_overlap(nums, first_len, second_len):
    s = list(accumulate(nums, initial=0))
    def solve(a, b):                  # a 段在前，b 段在后
        best_a = ans = 0
        for j in range(a + b, len(s)):
            # 以 j-b 结尾的前面，长为 a 的最大段和
            best_a = max(best_a, s[j - b] - s[j - b - a])
            ans = max(ans, best_a + s[j] - s[j - b])
        return ans
    return max(solve(first_len, second_len),
               solve(second_len, first_len))
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只算一种顺序：`firstLen` 的段可能在 `secondLen` 的段之后，要两种顺序都算。
- `best_a` 包含重叠的段：它必须结束在 `j - b` 之前，保证与 `b` 段不重叠。
- 前缀和下标差一：`s` 比 `nums` 多一位，`s[j] - s[j - b]` 才是以 `j` 结尾的长 `b` 的段。

**追问。**
- 三个不重叠子数组（LC 689）？：多一层「前缀最优 + 后缀最优」，枚举中间段。
- 为什么用一遍扫描就够？：每一时刻只需要「前面最优的 a 段」，它随 `j` 单调不减。

**同模式。** LC 1477 找两个和为目标值且不重叠的子数组、LC 53 最大子数组和

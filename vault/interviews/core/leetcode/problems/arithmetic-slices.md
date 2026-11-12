---
slug: arithmetic-slices
---
## Q
**LC 413 等差数列划分**｜Medium

统计 `nums` 中长度至少为 3 的等差子数组（连续）个数。

## A
**一句话。** 记「以当前元素结尾的等差子数组数」，公差延续就加一并累加进答案，公差断了清零。

```python
def number_of_arithmetic_slices(nums):
    ans = cur = 0     # cur：以 i 结尾的个数
    for i in range(2, len(nums)):
        if nums[i] - nums[i-1] == nums[i-1] - nums[i-2]:
            cur += 1
            ans += cur
        else:
            cur = 0
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 公差断开不清零：`[1,2,3,8,9,10]` 得 `3`，应为 `2`。
- 累加写在 `if` 外：公差不同的位置也加旧的 `cur`，结果偏大。

**追问。**
- 为什么 `cur` 加一就够？：以 `i` 结尾比以 `i-1` 结尾多一个（从最远起点延伸）加新的 3 元素那个。
- 允许不连续（子序列）呢？：`dp[i][d]` 记以 `i` 结尾公差为 `d` 的个数，用字典（LC 446）。

**同模式。** LC 446 等差数列划分 II - 子序列、LC 1027 最长等差数列、LC 978 最长湍流子数组、LC 53 最大子数组和

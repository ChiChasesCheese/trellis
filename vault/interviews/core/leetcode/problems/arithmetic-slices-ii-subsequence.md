---
slug: arithmetic-slices-ii-subsequence
---
## Q
**LC 446 等差数列划分 II - 子序列**｜Hard

整数数组 `nums`，统计所有长度至少为 3、且相邻元素之差相同的子序列的个数（子序列按下标选取，值相同但下标不同算不同）。

## A
**一句话。** `dp[i][d]` 是以 `nums[i]` 结尾、公差为 `d`、长度至少为 2 的等差子序列个数；把 `i` 接在以 `j` 结尾的 `dp[j][d]` 后面，每一个都变成长度至少 3 的合法答案。

```python
def number_of_arithmetic_slices(nums):
    n = len(nums)
    dp = [defaultdict(int) for _ in range(n)]
    ans = 0
    for i in range(n):
        for j in range(i):
            d = nums[i] - nums[j]
            cnt = dp[j][d]       # 以 j 结尾、公差 d、长度 >= 2
            ans += cnt           # 接上 i 后长度 >= 3
            dp[i][d] += cnt + 1  # 再加上 (j, i) 这个长度为 2 的
    return ans
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n^2)`。

**易错点。**
- 只统计长度至少 3：`dp` 里包含长度为 2 的子序列，答案只累加 `cnt`，不含刚形成的长度为 2 的那一个。
- 公差用数组下标：公差范围很大，必须用哈希表。
- 把相同值当同一个元素去重：下标不同的相同值是不同的子序列。

**追问。**
- 和 LC 413（子数组）有什么区别？：那里要连续，一个计数就够；子序列不连续，必须按公差分状态。
- 公差溢出？：Python 无此问题，其他语言 `int` 相减可能溢出，要先转长整型。

**同模式。** LC 413 等差数列划分、LC 1027 最长等差数列、LC 873 最长的斐波那契子序列的长度、LC 300 最长递增子序列

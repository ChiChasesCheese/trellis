---
slug: longest-arithmetic-subsequence
---
## Q
**LC 1027 最长等差数列**｜Medium

整数数组 `nums`，求其中最长等差子序列（不要求连续）的长度。

## A
**一句话。** `f[j][d]` 是以 `nums[j]` 结尾、公差为 `d` 的最长长度；枚举前一个下标 `i`，`d = nums[j] - nums[i]`，从 `f[i][d]` 转移。

```python
def longest_arith_seq_length(nums):
    n = len(nums)
    # f[j][d]：以 j 结尾、公差 d 的最长长度，至少 1
    f = [defaultdict(lambda: 1) for _ in range(n)]
    ans = 2
    for j in range(n):
        for i in range(j):
            d = nums[j] - nums[i]
            f[j][d] = f[i][d] + 1       # 接在 i 后面
            ans = max(ans, f[j][d])
    return ans
```

**复杂度。** 时间 `O(n²)`，空间 `O(n²)`。

**易错点。**
- 公差当成数组下标：公差可为负且很大，用字典或偏移，不能直接当下标。
- 默认长度写 `0`：任何单个数长度是 `1`，接上一个就是 `2`，默认值应为 `1`。
- 只比较相邻元素：子序列不要求连续，必须枚举所有 `i < j`。

**追问。**
- 值域小时有别的做法吗？：`f[i][d]` 换成数组，下标 `d` 加偏移，常数更小。
- 和 LC 300 最长递增子序列的联系？：都是「以某位置结尾」的子序列 DP，这里多一个公差维度。

**同模式。** LC 873 最长的斐波那契子序列的长度、LC 446 等差数列划分 II - 子序列、LC 300 最长递增子序列

---
slug: maximum-length-of-repeated-subarray
---
## Q
**LC 718 最长重复子数组**｜Medium

给两个整数数组，求公共的、连续的最长子数组的长度。

## A
**一句话。** 二维 DP：`dp[i][j]` 是以两数组当前元素结尾的最长公共子数组，相等则左上角加一，不等归零。

```python
def find_length(nums1, nums2):
    m, n = len(nums1), len(nums2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    best = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if nums1[i - 1] == nums2[j - 1]:
                dp[i][j] = dp[i-1][j-1] + 1  # 接在上一对后面
                best = max(best, dp[i][j])
            # 不等保持 0：子数组必须连续
    return best                              # 全表最大值
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 当成子序列用 `max(dp[i-1][j], dp[i][j-1])`：`([1,2,3],[1,3])` 得 `2`，应为 `1`。
- 不等时沿用左上角：`[0,1,0]` 与 `[0,0,0]` 得 `2`，应为 `1`。
- 答案取 `dp[m][n]`：子数组可在任意位置结束，示例 1 得 `0`，应为 `3`。

**追问。**
- 长度到 `10^5` 怎么办？：对长度二分（单调），每次用滚动哈希检查是否有公共窗口，`O(n log n)`。
- 改成最长公共子序列（LC 1143）？：转移改 `max`，答案取 `dp[m][n]`。

**同模式。** LC 1143 最长公共子序列、LC 72 编辑距离、LC 5 最长回文子串、LC 583 两个字符串的删除操作

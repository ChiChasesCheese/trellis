---
slug: length-of-longest-fibonacci-subsequence
---
## Q
**LC 873 最长的斐波那契子序列的长度**｜Medium

严格递增的正整数数组 `arr`，求最长的斐波那契式子序列的长度（`x[i] + x[i+1] = x[i+2]`，至少 3 项），没有返回 `0`。

## A
**一句话。** `f[j][k]` 是以 `arr[j]`、`arr[k]` 结尾的最长长度；前一项值 `arr[k] - arr[j]` 用哈希表找下标 `i`，要求 `i < j`。

```python
def len_longest_fib_subseq(arr):
    idx = {x: i for i, x in enumerate(arr)}
    n = len(arr)
    f = [[2] * n for _ in range(n)]   # f[j][k]：以 j, k 结尾
    ans = 0
    for k in range(n):
        for j in range(k):
            i = idx.get(arr[k] - arr[j], -1)
            if 0 <= i < j:            # 前一项必须在 j 前面
                f[j][k] = f[i][j] + 1
                ans = max(ans, f[j][k])
    return ans
```

**复杂度。** 时间 `O(n²)`，空间 `O(n²)`。

**易错点。**
- 不检查 `i < j`：`arr[k] - arr[j]` 可能大于 `arr[j]`，下标在 `j` 之后就不是子序列。
- 默认值写 `0`：任意两个数都可成为长度 `2` 的起点，初值是 `2`，只有 `≥ 3` 才返回。

**追问。**
- 为什么数组严格递增很重要？：保证值到下标唯一，哈希表能一步定位。
- 能不能不用哈希表？：对每个 `k` 用双指针找和为 `arr[k]` 的一对 `(i, j)`，同样 `O(n²)`。

**同模式。** LC 1027 最长等差数列、LC 413 等差数列划分、LC 300 最长递增子序列

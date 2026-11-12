---
slug: partition-array-for-maximum-sum
---
## Q
**LC 1043 分隔数组以得到最大和**｜Medium

把数组分成若干长度至多为 `k` 的连续段，每段的值都变成该段最大值，求变换后总和的最大值。

## A
**一句话。** 线性分段 DP：枚举最后一段的长度，贡献 `长度 × 段最大值`，向前扩段时滚动维护最大值。

```python
def max_sum_after_partitioning(arr, k):
    n = len(arr)
    dp = [0] * (n + 1)            # dp[i]：前 i 个的最大和
    for i in range(1, n + 1):
        seg_max = 0
        for length in range(1, min(k, i) + 1):
            seg_max = max(seg_max, arr[i - length])
            dp[i] = max(dp[i],
                        dp[i - length] + seg_max * length)
    return dp[n]
```

**复杂度。** 时间 `O(nk)`，空间 `O(n)`。

**易错点。**
- 每段都取满 `k`：`[1,15,7,9,2,5,10]`、`k=3` 得 `82`，应为 `84`。
- 下标错位：`dp` 长 `n+1`，最后一段第 `length` 个元素是 `arr[i - length]`，不是 `arr[i - length + 1]`。

**追问。**
- 每段必须恰好 `k`？：切法唯一，不需要 DP，逐段累加。
- 改成「变成段内最小值」？：每个元素自成一段最优，答案就是 `sum(arr)`。

**同模式。** LC 139 单词拆分、LC 91 解码方法、LC 1105 填充书架、LC 1335 工作计划的最低难度

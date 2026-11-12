---
slug: predict-the-winner
---
## Q
**LC 486 预测赢家**｜Medium

两人轮流从 `nums` 的任一端取一个数，各自求总分最大，玩家 1 先手。玩家 1 的分数大于等于玩家 2（平局算赢）返回 `true`。

## A
**一句话。** 区间 DP：`dp[i][j]` 是只剩 `nums[i..j]` 时先手的分差，取一端后减去对手的分差。

```python
def predict_the_winner(nums):
    n = len(nums)
    dp = [[0] * n for _ in range(n)]   # 先手得分 - 后手得分
    for i, x in enumerate(nums):
        dp[i][i] = x
    for length in range(2, n + 1):     # 区间长度从小到大
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(nums[i] - dp[i+1][j],
                           nums[j] - dp[i][j-1])
    return dp[0][n-1] >= 0             # 平局算先手赢
```

**复杂度。** 时间 `O(n²)`，空间 `O(n²)`。

**易错点。**
- 贪心取两端较大的：`[1,5,233,7]` 得 `false`，应为 `true`。
- 平局判成输（写成 `> 0`）：`[3,3]` 应返回 `true`。
- 递推里「加」对手的分差而不是「减」：表变成区间和，永远非负，`[1,5,2]` 误判 `true`。

**追问。**
- 先手的最高得分是多少？：`(sum(nums) + dp[0][n-1]) // 2`。
- 偶数个数时呢？：先手总能拿下全部奇数位或全部偶数位，必不输（LC 877）。

**同模式。** LC 877 石子游戏、LC 375 猜数字大小 II、LC 1140 石子游戏 II、LC 312 戳气球

---
slug: new-21-game
---
## Q
**LC 837 新 21 点**｜Medium

爱丽丝从 0 分开始，只要分数小于 `k` 就抽一次数，每次从 `[1, max_pts]` 等概率抽一个整数加到分数上；分数达到 `k` 或更高就停。求最终分数不超过 `n` 的概率。

## A
**一句话。** `dp[i]` 是恰好到达分数 `i` 的概率，它等于前面 `max_pts` 个、且分数小于 `k`（还会继续抽）的位置的概率和除以 `max_pts`；用滑动窗口维护这个和。

```python
def new21_game(n, k, max_pts):
    if k == 0 or n >= k + max_pts - 1:
        return 1.0               # 一定不会超过 n
    dp = [0.0] * (n + 1)
    dp[0] = 1.0
    window, ans = 1.0, 0.0       # window：能走到 i 的、未停的位置概率和
    for i in range(1, n + 1):
        dp[i] = window / max_pts
        if i < k:
            window += dp[i]      # 还会继续抽，可以作为跳板
        else:
            ans += dp[i]         # 到这里就停了，计入答案
        if 0 <= i - max_pts < k:
            window -= dp[i - max_pts]   # 滑出窗口
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 窗口里放了 `i >= k` 的位置：分数达到 `k` 就不再抽，它们不能转移给后面。
- 不处理 `k = 0` 或 `n` 足够大：这些情形概率恒为 1，且避免数组越界。
- 减窗口时不判下标范围：`i - max_pts` 可能为负，或本来就没加入过窗口。

**追问。**
- 不用滑动窗口，朴素转移是多少？：每个 `dp[i]` 累加 `max_pts` 项，`O(n · max_pts)`。
- 为什么不超过 `k + max_pts - 1`？：最后一次抽之前分数最大是 `k - 1`，再抽最多 `max_pts`。

**同模式。** LC 1155 掷骰子等于目标和的方法数、LC 688 骑士在棋盘上的概率

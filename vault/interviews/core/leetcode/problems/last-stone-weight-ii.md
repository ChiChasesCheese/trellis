---
slug: last-stone-weight-ii
---
## Q
**LC 1049 最后一块石头的重量 II**｜Medium

每回合任选两块石头粉碎（相等都消失，否则剩差值）。求最后剩下石头的最小可能重量，没有则为 `0`。

## A
**一句话。** 结果是带正负号的代数和，等价于分成两堆使差最小：0/1 背包求不超过 `总重//2` 的最大可达和。

```python
def last_stone_weight_ii(stones):
    n, total = len(stones), sum(stones)
    half = total // 2
    # dp[i][s]：前 i 块能否凑出总重 s
    dp = [[False] * (half + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for i in range(1, n + 1):
        w = stones[i - 1]
        for s in range(half + 1):
            dp[i][s] = dp[i-1][s] or (
                s >= w and dp[i-1][s-w])
    best = max(s for s in range(half + 1) if dp[n][s])
    return total - 2 * best
```

**复杂度。** 时间 `O(n·total)`，空间 `O(n·total)`。

**易错点。**
- 贪心每次砸最重两块：`[31,26,33,21,40]` 得 `9`，应为 `5`。
- 转移读本行 `dp[i][s-w]`：一块石头被用多次，`[1,3]` 得 `0`，应为 `2`。
- 漏设 `dp[0][0] = True`：整张表全 `False`，`max()` 抛 `ValueError`。

**追问。**
- 要输出具体分组？：从 `dp[n][best]` 回走，`dp[i-1][s]` 为真则不选第 `i` 块，否则选并 `s -= w`。
- 能更快吗？：用整数当位集，每块石头 `bits |= bits << w`。

**同模式。** LC 416 分割等和子集、LC 494 目标和、LC 474 一和零、LC 1046 最后一块石头的重量

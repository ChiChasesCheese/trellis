---
slug: maximum-points-you-can-obtain-from-cards
---
## Q
**LC 1423 可获得的最大点数**｜Medium

一行卡牌，每次从开头或末尾拿一张，恰好拿 `k` 张，求点数之和的最大值。

## A
**一句话。** 留下的是长为 `n-k` 的连续中段，滑动窗口求最小窗口和，用总和减去它。

```python
def max_score(card_points, k):
    n = len(card_points)
    w = n - k                     # 留下的中段长度
    cur = sum(card_points[:w])
    smallest = cur
    for i in range(w, n):         # 加入右端、移出左端
        cur += card_points[i] - card_points[i - w]
        smallest = min(smallest, cur)
    return sum(card_points) - smallest
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 窗口长度写成 `k`：留下的才是 `n-k`，写成 `k` 求的是「拿中间 `k` 张」。
- 每次贪心拿两端较大的：`[1,2,3,4,5,6,1]`、`k=3` 得 `6`，应为 `12`。

**追问。**
- 怎么还原具体拿法？：记录最小窗口起点 `s`，左边拿 `s` 张，右边拿 `k-s` 张。
- 两人轮流拿？：变成区间 DP `dp[l][r]`，见 LC 486 预测赢家。

**同模式。** LC 643 子数组最大平均数 I、LC 1658 将 x 减到 0 的最小操作数、LC 1004 最大连续 1 的个数 III、LC 209 长度最小的子数组

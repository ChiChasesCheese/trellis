---
slug: minimum-cost-for-tickets
---
## Q
**LC 983 最低票价**｜Medium

有 1 天、7 天、30 天三种票价 `costs`，给出严格递增的出行日 `days`，求覆盖所有出行日的最低花费。

## A
**一句话。** 按日期线性 DP：出行日从三种票各回退 1、7、30 天取最小，非出行日直接继承前一天。

```python
def min_cost_tickets(days, costs):
    travel = set(days)
    last = days[-1]
    dp = [0] * (last + 1)    # dp[d]：覆盖前 d 天出行日的最小花费
    for d in range(1, last + 1):
        if d not in travel:
            dp[d] = dp[d-1]
            continue
        dp[d] = min(dp[d-1] + costs[0],
                    dp[max(0, d-7)] + costs[1],
                    dp[max(0, d-30)] + costs[2])
    return dp[last]
```

**复杂度。** 时间 `O(max(days))`，空间 `O(max(days))`。

**易错点。**
- 回退下标不夹到 `0`：第 3 天读 `dp[-4]`，Python 负下标不报错，静默取到数组尾部。
- 非出行日也做三选一：白付票价，应直接继承 `dp[d-1]`。
- 7 日票覆盖 `d..d+7`：其实是 7 个自然日 `d..d+6`。

**追问。**
- 日期范围到 `10^9` 怎么办？：只对出行日做 DP，用 `bisect` 找回退位置，`O(n log n)`。
- 要输出买票方案？：记录每步选了哪种票，从末尾倒推。

**同模式。** LC 70 爬楼梯、LC 322 零钱兑换、LC 746 使用最小花费爬楼梯

---
slug: best-time-to-buy-and-sell-stock-ii
---
## Q
**LC 122 买卖股票的最佳时机 II**｜Medium

给每天的股价 `prices`，可买卖任意多次但同一时刻最多持有一股（可当天先卖再买），求最大利润。

## A
**一句话。** 贪心：每一段上涨都能拆成逐日差额，答案是所有相邻两天正差额之和。

```python
def max_profit(prices):
    # 相邻两天的差额，只吃涨的
    gains = (b - a for a, b in pairwise(prices))
    return sum(g for g in gains if g > 0)
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 当成只能交易一次（LC 121）：`[7,1,5,3,6,4]` 得 `5`，应为 `7`。
- 找谷买峰卖时漏掉末尾的上涨：循环提前退出，最后一个峰没卖。逐日差额没有这个边界。

**追问。**
- 每笔交易有手续费（LC 714）？：贪心失效，改 DP：`cash = max(cash, hold + p - fee)`，`hold = max(hold, cash - p)`。
- 卖出后冷却一天（LC 309）？：DP 多一个冷却状态。
- 至多 `k` 次交易（LC 188）？：状态加上交易次数，`O(nk)`；`k >= n/2` 时退化为本题。

**同模式。** LC 121 买卖股票的最佳时机、LC 123 买卖股票的最佳时机 III、LC 309 买卖股票的最佳时机含冷冻期、LC 714 买卖股票的最佳时机含手续费

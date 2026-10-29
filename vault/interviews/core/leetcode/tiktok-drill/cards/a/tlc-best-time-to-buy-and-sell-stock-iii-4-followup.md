---
id: tlc-best-time-to-buy-and-sell-stock-iii-4-followup
node: a.best-time-to-buy-and-sell-stock-iii
type: qa
step: 4
---
## Q
**LC 123 买卖股票的最佳时机 III**｜追问

面试官接着问：（1）最多 `k` 笔交易（LC 188）？（2）每次卖出后有一天冷冻期（LC 309）？（3）`k` 大于 `n / 2` 时有什么捷径？（4）要输出具体的买卖日期？

## A
1. **最多 `k` 笔**：每个"第几笔"开一对状态，`buy[t]`、`sell[t]`，每天对 `t = 1..k` 依次更新。时间 `O(n·k)`，空间 `O(k)`。

```python
def max_profit_k(k: int, prices: list[int]) -> int:
    buy = [-prices[0]] * (k + 1)
    sell = [0] * (k + 1)
    for p in prices:
        for t in range(1, k + 1):
            buy[t] = max(buy[t], sell[t - 1] - p)
            sell[t] = max(sell[t], buy[t] + p)
    return sell[k]
```

`max_profit_k(2, [3,3,5,0,0,3,1,4])` → `6`；`k = 2` 时与卡片中的四变量写法等价。
2. **冷冻期**：状态变成三个——持有、未持有且处于冷冻、未持有且可买入；卖出的那天转入冷冻，隔一天才能回到"可买入"。
3. **`k >= n // 2` 的捷径**：交易笔数已经不受限制（每两天最多一笔），退化成无限次交易（LC 122）：把所有正的相邻差值累加。这样避免开很大的数组。
4. **输出日期**：同时保存每个状态的"来源"，或者记录更新的天数，回溯时从 `sell2` 开始沿着转移链找回对应的买入、卖出日；也可以用前缀 / 后缀分解求出分界日，再各自找那一笔交易的起止。

**Python 提醒**：`[-prices[0]] * (k + 1)` 对整数安全；`k` 很大时两个数组也跟着变大，先 `k = min(k, len(prices) // 2)` 截断再开数组（交易笔数超过 `n // 2` 没有意义）。

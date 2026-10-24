---
id: tlc-patterns-dp-linear-4-stock
node: patterns.dp-linear
type: qa
step: 4
---
## Q
**动态规划：线性与状态机｜状态机 DP：买卖股票（LC 121、122）**

怎样用"持有 / 不持有"两个状态写买卖股票？一次交易与无限次交易的区别在哪个转移上？

## A
每天结束时只可能处于两种状态：**持有**一股（`hold`），或**不持有**（`cash`）。每个状态记录当前能得到的最大收益。

```python
def max_profit(prices: list[int]) -> int:
    lowest, best = prices[0], 0
    for p in prices[1:]:
        best = max(best, p - lowest)       # 今天卖出
        lowest = min(lowest, p)            # 今天之前的最低价（只买一次，买入时手上是 0）
    return best

def max_profit_ii(prices: list[int]) -> int:
    hold, cash = -prices[0], 0             # hold：持有的最大收益；cash：不持有的最大收益
    for p in prices[1:]:
        hold, cash = max(hold, cash - p), max(cash, hold + p)   # 今天买入 / 今天卖出
    return cash
```

运行：`max_profit([7,1,5,3,6,4])` → `5`，`[7,6,4,3,1]` → `0`；`max_profit_ii([7,1,5,3,6,4])` → `7`，`[1,2,3,4,5]` → `4`，`[7,6,4,3,1]` → `0`。时间 `O(n)`，空间 `O(1)`。

两题的差别只在买入时的"本金"：
- **一次交易**：买入时手上是 `0`，所以 `hold = max(hold, -p)`，等价于记录最低价。
- **无限次交易**：买入时手上是之前赚的 `cash`，所以 `hold = max(hold, cash - p)`。

扩展方式：**冷冻期**（卖出后隔一天才能买）、**手续费**、**最多 `k` 次交易** 都是在状态里多加一维或改转移，状态机思路不变：先画出状态之间的箭头，再写每个状态的最大收益。

- 同一天先更新 `hold` 还是先更新 `cash`：用元组赋值，右边都用旧值，避免同一天"买了又卖"。
- LC 122 还有等价的贪心：所有相邻上涨的差累加，`sum(max(0, b - a) for a, b in pairwise(prices))`。

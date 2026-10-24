---
id: tlc-best-time-to-buy-and-sell-stock-4-followup
node: a.best-time-to-buy-and-sell-stock
type: qa
step: 4
---
## Q
**LC 121 买卖股票的最佳时机**｜追问

面试官接着问：（1）要同时返回买入日和卖出日？（2）可以交易任意多次（先卖再买，同一时刻最多持有一股）？（3）价格以数据流的形式一个个到来，不能存整个数组？

## A
1. **返回买入日和卖出日**：多记一个最低价所在的下标 `low_day`；利润刷新时把 `(best, low_day, day)` 一起记下。`[7,1,5,3,6,4]` → 返回 `(5, 1, 4)`：下标 1 买入、下标 4 卖出，利润 `5`；`[7,6,4,3,1]` → 利润 `0`。
```python
def max_profit_days(prices: list[int]) -> tuple[int, int, int]:
    low_day = buy = sell = 0
    best = 0
    for day, p in enumerate(prices):
        if p < prices[low_day]:
            low_day = day
        if p - prices[low_day] > best:
            best, buy, sell = p - prices[low_day], low_day, day
    return best, buy, sell
```
2. **任意多次交易**（LC 122）：每一段上涨都拿到手，答案是所有相邻正差之和。`[7,1,5,3,6,4]` → `7`（`4 + 3`）。
```python
from itertools import pairwise

def max_profit_many(prices: list[int]) -> int:
    return sum(max(0, b - a) for a, b in pairwise(prices))
```
3. **数据流**：本来就是在线算法——只需 `low` 和 `best` 两个变量，来一个价格更新一次，`O(1)` 空间，不依赖随机访问。限制 `k` 次交易（LC 188）才需要 DP 状态数组。

**Python 提醒**：`itertools.pairwise` 要求 Python 3.10+，返回迭代器，对长度小于 2 的输入不产出任何元素，所以 `sum(...)` 自然得到 `0`；不要写成 `zip(prices, prices[1:])`，那会复制一份长度 `n` 的切片。

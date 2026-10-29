---
id: tlc-best-time-to-buy-and-sell-stock-ii-2-code
node: a.best-time-to-buy-and-sell-stock-ii
type: qa
step: 2
---
## Q
**LC 122 买卖股票的最佳时机 II**｜写出 Python 实现

整数数组 `prices`（长度 `1..3·10^4`，每个值 `0..10^4`）。不限交易次数，每次最多持有一股，同一天可以先卖后买。返回最大利润，不赚钱时为 `0`。要求 `O(n)`。

## A
**思路。** 任何一段连续上涨的利润都等于这段每天涨幅之和，而不限交易次数、允许当天买卖，所以可以把每一天的上涨都当成一次独立的「前一天买、今天卖」。下跌的日子不交易。答案就是所有相邻两天价差中为正的部分之和。

```python
def max_profit(prices: list[int]) -> int:
    # 每一段上涨都能吃到：把所有 “后一天比前一天高” 的差额加起来
    return sum(max(today - yesterday, 0) for yesterday, today in pairwise(prices))
```

运行：`prices=[7,1,5,3,6,4]` → `7`，`prices=[1,2,3,4,5]` → `4`，`prices=[7,6,4,3,1]` → `0`，`prices=[5]` → `0`，`prices=[2,2,2]` → `0`。

**复杂度。** 时间 `O(n)`，一遍扫描；空间 `O(1)`（`pairwise` 是惰性迭代器，不复制数组）。

**写法要点。** `itertools.pairwise(prices)`（Python 3.10+）产生相邻对 `(昨天, 今天)`，比 `zip(prices, prices[1:])` 少拷贝一份列表；生成器表达式 `sum(max(b - a, 0) ...)` 不建中间列表；`max(diff, 0)` 把下跌截断为 `0`。若面试官要看状态机，可以补一个等价的 DP：`cash, hold = max(cash, hold + p), max(hold, cash - p)`，元组赋值保证两个值都用旧状态。

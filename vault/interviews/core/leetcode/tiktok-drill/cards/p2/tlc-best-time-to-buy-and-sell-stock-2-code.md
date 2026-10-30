---
id: tlc-best-time-to-buy-and-sell-stock-2-code
node: p2.best-time-to-buy-and-sell-stock
type: qa
step: 2
---
## Q
**LC 121 买卖股票的最佳时机**｜写出 Python 实现

数组 `prices`（长度 `1` 到 `10^5`，每个价格在 `0` 到 `10^4`），只能买一次、卖一次且必须先买后卖，返回最大利润，无法获利返回 `0`。

## A
**思路。** 一遍扫描。`low` 是到当前为止见过的最低价；每一天都当作卖出日，利润是 `p - low`，取最大值。

```python
def max_profit(prices: list[int]) -> int:
    low, best = prices[0], 0          # low：迄今最低价
    for p in prices:
        low = min(low, p)
        best = max(best, p - low)
    return best
```

运行：`[7,1,5,3,6,4]` → `5`，`[7,6,4,3,1]` → `0`，`[5]` → `0`，`[3,10,1]` → `7`。

**复杂度。** 时间 `O(n)`：只扫一遍；空间 `O(1)`：只有两个变量。

**写法要点。** `low, best = prices[0], 0` 用元组一次初始化两个量；先 `low = min(low, p)` 再算利润，当天买当天卖利润为 `0`，所以不会出现负数，也不用写 `if`；`best` 初值 `0` 同时处理了「无法获利」。直接遍历值 `for p in prices` 比按下标取值更简洁。

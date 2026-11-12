---
slug: best-time-to-buy-and-sell-stock-iii
---
## Q
**LC 123 买卖股票的最佳时机 III**｜Hard

给每天股价 `prices`，最多完成两笔交易（先卖才能再买），求最大利润。

## A
**一句话。** 四个状态的状态机（第一次持有、卖出，第二次持有、卖出），每个状态只留当前最优现金。

```python
def max_profit(prices):
    buy1 = buy2 = -prices[0]   # 持有时的最大现金
    sell1 = sell2 = 0          # 卖出后的最大现金
    for p in prices:
        buy1 = max(buy1, -p)
        sell1 = max(sell1, buy1 + p)
        buy2 = max(buy2, sell1 - p)    # 用第一笔的利润再买
        sell2 = max(sell2, buy2 + p)
    return sell2
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 买入初值写成 `0`：相当于免费持股，`[7,6,4,3,1]` 得 `7`，应为 `0`。
- 先取最好一笔再取剩余区间：`[1,5,2,10]` 得 `9`，应为 `4 + 8 = 12`。

**追问。**
- 最多 `k` 笔（LC 188）？：`buy`、`sell` 各开 `k+1` 的数组，内层枚举笔数。
- 含冷冻期或手续费？：状态换成持有 / 未持有 / 冷冻，转移里加对应代价（LC 309、LC 714）。

**同模式。** LC 121 买卖股票的最佳时机、LC 122 买卖股票的最佳时机 II、LC 188 买卖股票的最佳时机 IV、LC 309 含冷冻期

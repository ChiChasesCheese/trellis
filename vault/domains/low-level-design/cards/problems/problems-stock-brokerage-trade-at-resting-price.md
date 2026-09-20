---
id: problems-stock-brokerage-trade-at-resting-price
node: problems.marketplaces.stock-brokerage
type: qa
step: 4
tags: [grown]
---
## Q
股票撮合里，一张限价买单出价 100、簿子上挂着一张 97 的卖单，两张单交叉了。成交打在 100、97 还是中间价？多出来的钱归谁？

## A
打在 **97——挂单方（passive / maker，先到并公开报价的那一方）的价**。差额退给来单方（aggressive / taker）。

理由：挂单方先到，它公布的价格是市场**已经承诺过**的价；来单方愿意出更好的条件是它自己的事。这叫价格改善（price improvement）。

流行题解（包括 geektrust 那道被真实面试用过的题面）写的是「永远按**卖单**的价成交」。它在「卖单先挂、买单后到」时碰巧等价，但在「买单先挂 237.80、更低的卖单 236.00 后到」时就错了：凭什么让早就承诺出 237.80 的买家只付 236.00？

记账上的体现是：冻结按限价，扣款按成交价，差额自动回到可用余额。

```python
def apply_buy(self, symbol, quantity, price, reserve_price):
    self.reserved_cash -= quantity * reserve_price
    self.cash -= quantity * price
    self._bump(self._positions, symbol, quantity)
```

由此还得到一条对称性：**挂单方永远按自己的价成交，所以它的预留被精确花光，只有来单方才有差额要退。**

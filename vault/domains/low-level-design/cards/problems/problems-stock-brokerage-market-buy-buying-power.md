---
id: problems-stock-brokerage-market-buy-buying-power
node: problems.marketplaces.stock-brokerage
type: qa
step: 5
tags: [grown]
---
## Q
股票交易系统里限价买单按限价冻结资金，那**市价买单**（market order，不带价、要求立即按对手方价格成交）拿什么算购买力？用「最新成交价」估一下行不行？

## A
不行。最新成交价是**过去**的价，簿子可能早就跳空了，按它冻结会冻少，成交时又得回滚。

正确做法：**先照着当前簿子试算一次（walk），按试算里最差的那一档价冻结**。

```python
def walk_cost(self, quantity: int) -> tuple[int, int]:
    remaining, worst = quantity, 0
    for price in self.asks.prices_in_priority():
        if remaining <= 0:
            break
        take = min(remaining, self.asks.quantity_at(price))
        remaining -= take
        if take:
            worst = price
    return quantity - remaining, worst
```

关键不在这段代码，而在**它和随后的撮合跑在同一把锁里**：试算不会过期，所以「按最差价冻结」一定够。冻多了的部分在逐笔成交时按真实价扣、当场退。

两个边界必须说清：簿子上能吃到的量不够整张单时，只为能吃到的部分冻钱，**剩余量随即作废——市价单永远不挂单**；空簿子上报市价单的结果是一张 0 成交的 CANCELLED 单，而不是异常（簿子空是市场状态，不是用户的过错）。

---
id: problems-stock-brokerage-status-enum-not-state-classes
node: problems.marketplaces.stock-brokerage
type: qa
step: 6
tags: [grown]
---
## Q
股票订单有 NEW → PARTIALLY_FILLED → FILLED / CANCELLED / REJECTED 五个状态，买卖还分两个方向。该不该用状态模式（State，每个状态一个类）和 `BuyOrder` / `SellOrder` 两个子类？

## A
**两个都不该。**

判据是「每个状态下**行为**差异有多大」。订单里受状态影响的行为只有一个：能不能撤。那就是一行 `if not order.status.is_terminal`。为它建 `OpenState` / `FilledState` / `CancelledState` 三个类，等于把一行 `if` 摊成三个文件，把「撤单规则」从一处搬到三处；将来加一个 EXPIRED 状态，要新增一个类还要改另外三个。`Enum` 加一个 `is_terminal` 属性表达的信息一模一样，而且能穷举、能打印、能直接进数据库。

```python
class OrderStatus(Enum):
    NEW = "new"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

    @property
    def is_terminal(self) -> bool:
        return self in (OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED)
```

用状态模式的真正信号是：状态之间行为差异大、每个状态要处理多种事件、状态数还会增长。订单一条都不满足。

`BuyOrder` / `SellOrder` 同理——买卖的差别是两三处 `if side is Side.BUY`，一个 `Side` 枚举（带 `opposite` 属性）就够，撮合循环还能两侧共用同一段代码。

还有一点：**没有 PARTIALLY_FILLED_AND_CANCELLED 这种状态**。撤掉一张成交了一半的单，状态就是 CANCELLED，成交了多少由 `filled_quantity` 说话——同一件事不要两份表示。

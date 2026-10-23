---
id: hft-architecture-order-state-states
node: architecture.order-state
type: qa
step: 1
---
## Q
一张订单从发出到结束，在交易系统里会经历哪些状态？

## A
订单是一个**状态机（state machine）**：任一时刻处于一种状态，收到事件才会转移。典型状态：
- **PENDING**：我们已发出，交易所还没回话。
- **WORKING**：交易所确认收下，订单挂在订单簿上等成交。
- **PARTIALLY_FILLED**：部分成交，还有剩余。
- **PENDING_CANCEL**：撤单请求已发出，还没有确认。
- 终态：**FILLED**（全部成交）、**CANCELED**（已撤）、**REJECTED**（被拒）。终态不再变化。

例：买 100 股 → PENDING → 收到确认 → WORKING → 成交 40 股 → PARTIALLY_FILLED（剩 60）→ 再成交 60 股 → FILLED。

---
id: hi-pt-beverage-vending-system-4-order-fsm
node: qb.lld.beverage-vending-system.points
type: qa
step: 3
---
## Q
**多地点饮品自助售卖系统 · 订单状态机与幂等**｜必会 · 出自：多地点饮品自助售卖系统 › 深入 2

支付回调、机器回调可能重复到达，订单状态怎么管理才不重复产生副作用？

## A
**要点。** 订单状态 `CREATED → RESERVED → BREWING → READY → PICKED_UP`，另有 `FAILED`、`EXPIRED`、`CANCELLED`。合法迁移集中在一张迁移表，非法迁移报错，任何服务不能直接改状态。
**幂等。** `move` 对「已在目标状态」返回 False，调用方据此不再执行副作用。

---
id: hi-pt-beverage-vending-system-5-failure
node: qb.lld.beverage-vending-system.points
type: qa
step: 4
---
## Q
**多地点饮品自助售卖系统 · 制作失败与机器离线**｜追问 · 出自：多地点饮品自助售卖系统 › 深入 3

制作失败、机器离线、中心与机器断网，订单、库存、退款各怎么处理？

## A
**失败。** 释放预留，订单 `FAILED`，退款服务订阅事件执行退款（事件至少一次，以订单号做幂等键）。
**离线。** 定时心跳，超时标记离线，其 `RESERVED` 订单批量转 `FAILED` 或重路由到同地点其他机器。
**断网。** 机器只执行已下发的订单，不接受离线新单。

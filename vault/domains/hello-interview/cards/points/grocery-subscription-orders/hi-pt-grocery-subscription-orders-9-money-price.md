---
id: hi-pt-grocery-subscription-orders-9-money-price
node: qb.lld.grocery-subscription-orders.points
type: qa
step: 10
---
## Q
**生鲜订阅转订单服务 · 金额与价格**｜加分 · 出自：生鲜订阅转订单服务 › 深入 4

订阅服务中金额怎么表示？订阅创建时要不要锁定价格？

## A
**金额。** 用整数分，避免浮点误差。
**价格。** 创建时不锁定，转换时按当时价格计算，用户通常期望按当前价。
**价格保护。** 若产品承诺价格保护，订阅里记录价格上限，超过则暂停并通知。

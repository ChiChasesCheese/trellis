---
id: hi-ov-flash-sale-2-options
node: sd.problem-breakdowns.flash-sale
type: qa
step: 2
tags: [通览]
---
## Q
**限时抢购 · 高层设计**｜通览

限时抢购的高层设计怎么搭？每个功能需求走哪条路径？

## A
**组件。** API 网关、抢购服务、Postgres、第三方支付方。

**每条路径。**
- **看商品：** `GET` 经网关到抢购服务，读 Postgres 里的商品与剩余数量。
- **预留一个单元：** 同一事务内检查库存、插入带过期时间的 Reservation、库存减一，返回 expiresAt；过期的由定时任务回收。
- **付款买下：** 服务确认预留未过期，建 PENDING 的 Purchase，向支付方创建 PaymentIntent；客户端直接向支付方付款，支付方用 webhook 通知结果；客户端轮询购买状态。

**存储。** Postgres 存商品、预留与购买，选它是为了事务正确性。

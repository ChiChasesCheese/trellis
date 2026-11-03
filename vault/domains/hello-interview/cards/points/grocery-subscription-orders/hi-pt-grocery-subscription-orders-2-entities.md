---
id: hi-pt-grocery-subscription-orders-2-entities
node: qb.lld.grocery-subscription-orders.points
type: qa
step: 2
---
## Q
**生鲜订阅转订单服务 · 核心类与职责**｜必会 · 出自：生鲜订阅转订单服务 › 核心实体与接口

订阅转订单服务应该划分哪些类？各自的职责和关键方法是什么？

## A
**类。** `Subscription`（items、every_days、next_run、状态）、`Order`（`(sub_id, cycle)` 幂等键、明细、总价、状态）、`Inventory`（`reserve` 整单全有或全无、`release` 归还）、`Wallet`（`debit` 余额不足返回失败）、`SubscriptionService`（`create`、`run_due(today)`、`_convert`）。
**模式。** 事务脚本加补偿（最小形式的 Saga）、仓储、可替换的履约策略。

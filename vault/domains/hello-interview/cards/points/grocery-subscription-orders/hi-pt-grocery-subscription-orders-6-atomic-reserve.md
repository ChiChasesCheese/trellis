---
id: hi-pt-grocery-subscription-orders-6-atomic-reserve
node: qb.lld.grocery-subscription-orders.points
type: qa
step: 6
---
## Q
**生鲜订阅转订单服务 · 库存的原子预留与锁顺序**｜出自：生鲜订阅转订单服务 › 深入 1

两个订阅同时抢仅剩一件的商品，怎样避免超卖？锁怎么细化而不死锁？持久化版本怎么做？

## A
**要点。** `reserve` 在一把锁内完成"检查全部明细、再扣减全部明细"，整单全有或全无。
**细化。** 规模变大后按商品加锁，必须按商品 ID 排序后逐个加锁，避免两个订单反序加锁而死锁。
**持久化。** 用条件更新代替内存锁：`UPDATE ... SET stock = stock - ? WHERE stock >= ?`，看影响的行数。

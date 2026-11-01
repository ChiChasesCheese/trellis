---
id: hi-pt-grocery-subscription-orders-3-idempotency-key
node: qb.lld.grocery-subscription-orders.points
type: qa
step: 3
---
## Q
**生鲜订阅转订单服务 · 幂等键 (sub_id, cycle)**｜出自：生鲜订阅转订单服务 › 整体设计

定时任务可能重跑同一天，如何保证同一个订阅的同一期不产生两个订单？

## A
**要点。** 订单以 `(sub_id, cycle)` 为唯一键。`_convert` 一开始先查这个键，已有订单就直接返回。
**测试。** 对同一天连续调用两次 `run_due`，第二次不产生新订单。
```python
key = (sub.id, cycle)
if key in self.orders:
    return self.orders[key]
```

---
id: problems-food-delivery-batch-has-no-state-machine
node: problems.marketplaces.food-delivery
type: qa
step: 6
tags: [grown]
---
## Q
外卖里一位骑手一次带走的两三单组成一个批次（batch）。要不要给批次也配一套状态机（CREATED → PICKING_UP → DELIVERING → DONE）？

## A
**不要。** 批次的状态就是其中每一单状态之和，另起一套只会多一份要对齐的真相：骑手取了两单里的一单，批次算 PICKING_UP 还是 DELIVERING？两份状态一旦不一致，你既不知道该信哪个，也说不清是谁写错的。

所以批次是一个 `frozen dataclass`——id、骑手、订单 id 的元组、创建时间，**没有任何方法**。「整个批次送完了吗」是一次对订单状态的查询：

```python
if all(orders[i].state is OrderState.DELIVERED for i in batch.order_ids):
    couriers.finish(batch.courier_id, order.dropoff)
    del self._batches[batch.id]
```

判据：**一个对象只有在它拥有别人不能回答的问题时，才需要自己的状态。**

顺带，上面那两行也是批次表唯一会缩小的地方——没有它，批次表会随每一单永久增长。每个容器都要能回答「谁在什么时候删我」。

---
id: hi-pt-dasher-payout-2-heap-concurrency
node: qb.lld.dasher-payout.points
type: qa
step: 2
---
## Q
**配送员报酬计算 · 接单时在途数**｜必会 · 出自：配送员报酬计算 › 深入 2

每单的倍率取决于"接单那一刻还有几单在途"。怎样在 O(n log n) 内对所有订单算出这个数？

## A
**做法。** 订单按接单时间排序；堆里放在途订单的结束时间，每到一个新订单，先弹出结束时间不晚于它接单时间的，堆的大小就是接单时的在途数。

```python
while ongoing and ongoing[0] <= d.accepted:
    heapq.heappop(ongoing)
multiplier = plan.multiplier(len(ongoing))
heapq.heappush(ongoing, d.ended)
```
**为什么。** 时间只往前走，弹出的订单不会再有效（惰性删除），每单进出堆各一次。1,000 单约 1,000 x 10 次，而逐对比较约 1,000,000 次。

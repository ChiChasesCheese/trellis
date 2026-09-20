---
id: problems-food-delivery-batched-mip-vs-greedy-dispatch
node: problems.geo.food-delivery
type: qa
step: 4
tags: [grown]
---
## Q
In a food delivery courier dispatch design, why is assigning each newly confirmed order to "the single nearest available courier" (greedy nearest-match) systematically not optimal for the whole marketplace, even though it is locally optimal for that one order?

## A
Greedy nearest-match commits a courier to one order immediately, which can mean the courier misses a different order that appears moments later and would have been closer, forcing either a detour back or assigning that new order to a farther courier instead. It also completely misses batching: if two orders share a nearby pickup or drop-off, one courier picking up both in a single trip cuts courier-time cost roughly in half compared to sending two separate couriers, but greedy per-order assignment never considers pairing orders together because it decides one order at a time. A periodic batched optimizer that jointly considers all orders confirmed and all couriers online within a short window can find these batching opportunities and avoid the myopic mistakes that come from deciding one order in isolation.

## Q zh
在外卖骑手调度设计中，为什么把每个新确认的订单指派给「当前最近的空闲骑手」（贪心最近匹配）对整个市场来说系统性地不是最优的，即便这对单独这一单来说是局部最优的？

## A zh
贪心最近匹配会立刻把一个骑手绑定给一单，这可能导致这个骑手错过几分钟后出现、其实离他更近的另一单，迫使他要么绕路回来，要么这个新订单被指派给一个更远的骑手。它还完全错过了打包（batching）的机会：如果两个订单的取餐点或送达点相近，一个骑手一趟取送两单，比派两个骑手各跑一单节省了近一半的骑手时间成本，但逐单贪心指派永远不会考虑把订单配对，因为它每次只决定一单。一个周期性运行、同时考虑一个短窗口内所有已确认订单和所有在线骑手的批量优化器，能发现这些打包机会，避免逐单孤立决策带来的短视错误。

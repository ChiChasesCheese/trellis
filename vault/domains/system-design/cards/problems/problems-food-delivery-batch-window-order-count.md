---
id: problems-food-delivery-batch-window-order-count
node: problems.geo.food-delivery
type: qa
step: 5
tags: [grown]
---
## Q
In a food delivery design where the busiest single market handles about 24 orders per second at its national peak minute and the dispatch service batches orders every 5 seconds, roughly how many orders sit in a single dispatch batch, and why does that number matter for choosing a real optimization solver over a pure heuristic?

## A
At about 24 orders/second over a 5-second window, a single batch holds on the order of 120 orders (24 * 5 = 120) to be jointly matched against the couriers currently online in that market. A problem of that size — even at the busiest market's busiest minute — is well within what a mixed-integer programming solver can solve within a dispatch cycle's time budget, which is why batching orders and couriers into one joint optimization problem is computationally practical rather than just theoretically appealing; a design shouldn't default to a pure heuristic out of an assumption that the batch would be too large to solve exactly.

## Q zh
在一个外卖配送设计中，假设全国最繁忙的单个市场在峰值分钟的订单速率约为每秒 24 单，调度服务每 5 秒批量处理一次订单，一次调度批次里大约有多少订单？这个数字为什么关系到该选用真正的优化求解器而不是纯启发式方法？

## A zh
在约每秒 24 单、5 秒窗口的条件下，一个批次大约有 120 单（24×5=120）需要和当前在该市场在线的骑手一起联合匹配。即便是全国最繁忙市场最繁忙的那一分钟，这个规模的问题也完全在混合整数规划（MIP）求解器能在一次调度周期的时间预算内求解的范围之内——这正是「把订单和骑手打包成一个联合优化问题」在计算上可行、而不只是理论上好看的原因；不应该因为假设批次规模求不动精确解，就默认退回纯启发式方法。

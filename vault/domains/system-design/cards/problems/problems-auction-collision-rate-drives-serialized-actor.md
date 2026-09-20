---
id: problems-auction-collision-rate-drives-serialized-actor
node: problems.commerce.auction
type: qa
step: 2
tags: [grown]
---
## Q
A hot online auction receives bids at 50 bids/sec in its final seconds, and each single-row conditional write to update the current highest bid takes about 5ms to commit. Modeling arrivals within one 5ms commit window as Poisson with mean mu = 50 x 0.005 = 0.25, the probability that 2 or more bids land in the same commit window is about 2.65%, giving roughly 5.3 colliding windows per second (200 windows/sec x 2.65%). Why does this number push the design toward routing all bids for one auction to a single serialized writer, instead of relying on plain optimistic conditional writes with client-side retry?

## A
5.3 collision-windows per second is not a rare edge case, it's roughly one collision every 190ms during the busiest second — meaning a meaningful fraction of bidders would need a full failed-write, re-read-current-price, re-submit round trip right when the confirmation latency budget is tightest. Routing every bid for that auction to one in-memory, single-threaded actor resolves who's leading before any durable write happens, so the write itself never fails due to a concurrent bid; it can only be rejected by business logic (the bid was too low), which needs no retry loop.

## Q zh
一场热门在线拍卖在最后几秒的出价到达速率是 50 次/秒，更新当前最高价的单行条件写提交耗时约 5ms。把一个 5ms 提交窗口内的到达建模为泊松分布，均值 μ = 50 × 0.005 = 0.25，则该窗口内出现 2 个或更多出价的概率约为 2.65%，对应每秒约 5.3 次冲突窗口（200 个窗口/秒 × 2.65%）。为什么这个数字会把设计推向“把同一场拍卖的所有出价路由到单一序列化写者”，而不是依赖普通的乐观条件写加客户端重试？

## A zh
每秒 5.3 次冲突窗口不是罕见的边缘情况，而是最繁忙的那一秒里大约每 190 毫秒就发生一次——意味着相当一部分出价者会在确认延迟预算最紧张的时刻，经历一次完整的“写入失败 → 重新读取当前价 → 重新提交”往返。把同一场拍卖的所有出价路由到一个内存中的单线程 actor，能在任何持久化写入发生之前就先判断出谁领先，所以写入本身永远不会因为并发出价而失败，只会被业务逻辑判定为“出价不够高”而直接拒绝，不需要重试循环。

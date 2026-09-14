---
id: traffic-request-hedging
node: traffic.load-balancing
type: qa
---
## Q
Request hedging: mechanism, the cost math that makes it cheap, and its prerequisites?

## A
If no reply arrives within roughly the **p95 latency**, send the same request to a second replica; take whichever answers first and cancel the other. The user's tail becomes the *min* of two draws — tail events (GC pause, slow disk) rarely strike both replicas.

Cost math: hedging only after p95 means ≤5% of requests are duplicated — ~5% extra load buys an order-of-magnitude better p99.

Prerequisites: idempotent (or deduplicated) operations, cross-replica cancellation, and never hedging a hedge — otherwise overload turns it into a self-amplifying storm.

## Q zh
请求对冲：机制、使其廉价的成本数学和先决条件？

## A zh
如果没有回复在大约 **p95 延迟**内到达，发送相同请求到第二个副本；取先回答的并取消另一个。用户的尾部变成两个抽取的*最小值* — 尾部事件（GC 暂停、缓慢磁盘）很少同时打击两个副本。

成本数学：对冲仅在 p95 后意味着 ≤5% 的请求被重复 — 约 5% 额外负载买单数量级更好的 p99。

先决条件：幂等（或去重）操作、跨副本取消，永不对冲对冲 — 否则过载将其变成自放大风暴。

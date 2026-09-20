---
id: problems-distributed-cache-sharding-tradeoffs
node: problems.foundations.distributed-cache
type: qa
step: 3
tags: [grown]
---
## Q
In a distributed cache, what does client-side sharding, a proxy layer (like mcrouter), and Redis Cluster's built-in hash-slot protocol each make pay the cost of a topology change?

## A
Client-side sharding embeds the shard map directly in each application process — lowest latency (no extra hop), but every process must receive and apply topology updates promptly, or it routes to the wrong node. A proxy layer centralizes the shard map in a stateless, horizontally-scalable proxy tier — application code stays simple and topology changes are transparent to it, at the cost of one extra network hop per request. Redis Cluster embeds sharding in the protocol itself: keys hash into one of 16384 fixed slots, and a client contacting the wrong node gets a `-MOVED` redirect telling it the right one, so no client needs the full topology upfront and no separate proxy tier is needed, at the cost of a redirect round-trip during migrations.

## Q zh
在分布式缓存中，客户端分片、代理层（如 mcrouter）和 Redis Cluster 内建的哈希槽协议，各自把拓扑变化的代价转嫁给了谁？

## A zh
客户端分片把分片映射直接嵌入每个应用进程——延迟最低（没有额外跳数），但每个进程都必须及时收到并应用拓扑更新，否则会路由到错误的节点。代理层把分片映射集中在一层无状态、可水平扩展的代理里——应用代码保持简单，拓扑变化对它透明，代价是每次请求多一跳网络往返。Redis Cluster 把分片内建在协议里：key 哈希到 16384 个固定槽位之一，联系错节点的客户端会收到 `-MOVED` 重定向告知正确节点，因此客户端不需要预先知道完整拓扑，也不需要独立的代理层，代价是迁移期间的重定向往返。

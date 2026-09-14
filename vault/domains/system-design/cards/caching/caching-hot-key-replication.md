---
id: caching-hot-key-replication
node: caching.placement
type: qa
---
## Q
One cache key (a celebrity's profile during an event) exceeds what a single cache node can serve. Why doesn't adding nodes help, and what does?

## A
Sharding places each key on exactly **one** node — more nodes just move the key; that node's NIC and CPU still cap the key's throughput.

- **Key replication**: write the value under R suffixed copies (`key#1..#R`), readers pick one at random — R× read capacity, at the cost of R× invalidation fan-out and R-way brief inconsistency.
- **Local L1 for the hottest set**: an in-process cache with second-level TTLs absorbs most reads before they reach the shared tier ([[caching-local-vs-remote]]).

Detect hot keys by sampling key frequency at the client — before the node melts, not after.

## Q zh
一个缓存键（事件期间名人的个人资料）超过了单个缓存节点可以服务的范围。为什么添加节点没有帮助，什么有用？

## A zh
分片将每个键放在恰好 **一个** 节点上 — 更多节点只是移动键；该节点的 NIC 和 CPU 仍然限制键的吞吐量。

- **键复制**：在 R 个后缀副本（`key#1..#R`）下写入值，读者随机选择一个 — R× 读容量，代价是 R× 失效扇出和 R 向简要不一致。
- **最热集合的本地 L1**：一个进程内缓存，带有二级 TTL 在到达共享层之前吸收大多数读（[[caching-local-vs-remote]]）。

通过在客户端采样键频率来检测热键 — 在节点熔化之前，而不是之后。

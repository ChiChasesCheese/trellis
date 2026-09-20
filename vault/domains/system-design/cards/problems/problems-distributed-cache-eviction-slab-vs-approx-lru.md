---
id: problems-distributed-cache-eviction-slab-vs-approx-lru
node: problems.foundations.distributed-cache
type: qa
step: 4
tags: [grown]
---
## Q
In a distributed cache node under memory pressure, why does a single global, exact LRU linked list not scale, and what do Memcached and Redis each do instead?

## A
An exact global LRU requires moving a node in a shared linked list on every access, which becomes a lock-contention bottleneck on a multithreaded server and violates tight P99 latency budgets. Memcached instead partitions memory into fixed-size slab classes; eviction happens only within the slab class a value belongs to, avoiding any single global structure, at the cost of internal fragmentation (a value wastes the unused remainder of its slab class's size). Redis instead avoids any linked list: it stores an access timestamp per key and, on eviction, randomly samples a small number of keys and evicts the least-recently-used one among the sample, repeating until enough memory is freed — approximate rather than exact, but with no global locking structure at all.

## Q zh
在内存压力下的分布式缓存节点中，为什么一条全局精确的 LRU 链表无法扩展？Memcached 和 Redis 各自用什么替代它？

## A zh
精确的全局 LRU 要求每次访问都在一条共享链表上做移动操作，这在多线程服务器上会变成锁竞争瓶颈，违反紧张的 P99 延迟预算。Memcached 的做法是把内存划分成固定大小的 slab class，驱逐只发生在值所属的那个 slab class 内部，避免了任何全局结构，代价是内部碎片（一个值会浪费它所在 slab class 未用满的剩余空间）。Redis 的做法是完全不用链表：为每个 key 存一个访问时间戳，驱逐时随机采样少量 key，淘汰采样里最久未访问的一个，重复几轮直到腾出足够空间——是近似而非精确，但完全没有全局锁定结构。

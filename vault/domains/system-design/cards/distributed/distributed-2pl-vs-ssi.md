---
id: distributed-2pl-vs-ssi
node: distributed.transactions.concurrency-control
type: qa
---
## Q
Two-phase locking vs serializable snapshot isolation — how does each achieve serializability, what does each cost, and when does each win?

## A
- **2PL (pessimistic)**: acquire shared locks to read, exclusive to write, hold **all** locks until commit. Readers block writers and vice versa; cost = deadlocks (detected → abort) and terrible latency variance when anything queues behind a long transaction.
- **SSI (optimistic)**: run everything on an MVCC snapshot without blocking; track **read-write dependencies** between concurrent transactions and, at commit, abort one whenever a dangerous structure (potential cycle) appears. Cost = abort-and-retry work, which explodes under contention.

Choose 2PL-style pessimism when conflicts are frequent (hot rows — retrying is wasted work); SSI when the workload is mostly reads or conflicts are rare. Postgres `SERIALIZABLE` is SSI; classic SQL Server serializable is 2PL.

## Q zh
两阶段锁（2PL）和可串行化快照隔离（SSI）——各自如何实现可串行化？各自的代价是什么？各自什么时候胜出？

## A zh
- **2PL（悲观）**：读取时获取共享锁，写入时获取排他锁，**所有**锁一直持有到提交。读阻塞写，写也阻塞读；代价 = 死锁（检测到后中止）以及排在长事务后面时糟糕的延迟方差。
- **SSI（乐观）**：所有操作都在 MVCC 快照上运行、不加锁；跟踪并发事务之间的**读写依赖**，在提交时一旦出现危险结构（潜在的环）就中止其中一个。代价 = 中止重试的开销，在高争用下会爆炸式增长。

冲突频繁时（热点行——重试是浪费的工作）选择 2PL 式的悲观策略；工作负载以读为主或冲突罕见时选择 SSI。Postgres 的 `SERIALIZABLE` 是 SSI；经典的 SQL Server 可串行化是 2PL。

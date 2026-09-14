---
id: distributed-deadlock-handling
node: distributed.transactions.concurrency-control
type: qa
---
## Q
Under 2PL, what makes the deadlock rate explode, how do engines resolve deadlocks, and what do you change in the application?

## A
Rate scales viciously: deadlock frequency grows roughly with **concurrency squared and transaction length to the fourth power**, divided by the number of distinct lockable items (Gray's classic estimate). Practical reading: doubling the statements inside a transaction hurts ~16x more than doubling the number of clients — **long transactions are the problem**, not load.

Resolution, two families:

- **Detection**: build the waits-for graph, find a cycle, kill the cheapest victim (InnoDB's detector; it can be disabled at very high concurrency, falling back to `innodb_lock_wait_timeout`, default 50 s). Victim gets a retryable error.
- **Prevention by priority**: order transactions by start timestamp and never let a cycle form — **wound-wait** (older transaction wounds the younger holder) or wait-die; CockroachDB and Spanner-style systems use this, since a distributed waits-for graph is expensive to build.

Application fixes: acquire locks in a **consistent global order** (sort ids before updating), shorten transactions (never hold a lock across an RPC or user think-time), and make every write path **retryable and idempotent**.

## Q zh
在 2PL 下，是什么让死锁率爆炸式增长？引擎是怎样解决死锁的？应用层要做出什么改变？

## A zh
死锁率的增长非常凶猛：死锁频率大致随**并发度的平方、事务长度的四次方**增长，再除以可加锁对象的数量（Gray 的经典估计）。实践上的理解是：把一个事务里的语句数翻倍，造成的伤害大约是把客户端数量翻倍的 16 倍——**长事务才是问题所在**，而不是负载本身。

解决方案分两类：

- **检测**：构建等待图（waits-for graph），找环，杀掉代价最小的那个受害者（InnoDB 的检测器；在极高并发下可以关闭，退回到 `innodb_lock_wait_timeout`，默认 50 秒）。受害者会得到一个可重试的错误。
- **按优先级预防**：按事务的起始时间戳排序，永远不让环形成——**wound-wait**（更老的事务"击伤"更年轻的锁持有者）或 wait-die；CockroachDB 和 Spanner 风格的系统用这种方式，因为构建一个分布式的等待图代价太高。

应用层的修复：按**一致的全局顺序**获取锁（更新前先给 id 排序）、缩短事务（永远不要在一次 RPC 或用户思考时间内还持有锁），并让每条写路径都**可重试且幂等**。

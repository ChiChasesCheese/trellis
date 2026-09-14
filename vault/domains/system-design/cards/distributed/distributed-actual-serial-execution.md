---
id: distributed-actual-serial-execution
node: distributed.transactions.concurrency-control
type: qa
---
## Q
Besides 2PL and SSI there is a third road to serializability: actually executing transactions serially, one at a time on a single thread (VoltDB/H-Store; Redis works this way too). What makes this viable at all, and what three conditions must hold?

## A
Viable because removing concurrency removes **all** concurrency-control overhead — no locks, no deadlocks, no aborts-and-retries — and a single core plowing through in-memory data is far faster than the folklore suggests; serializability is trivially guaranteed by construction.

Conditions:
- **Data fits in RAM**: one transaction touching disk would stall the *only* thread and every queued transaction behind it.
- **Transactions are short and non-interactive**: submitted as a whole (stored procedures), never waiting mid-transaction for an application round-trip or user input — any pause blocks the world.
- **Throughput fits one core per partition**: scale by partitioning the data, one serial executor each; but a **cross-partition transaction** then needs coordination across executors and is orders of magnitude slower — so the workload must be partitionable so that most transactions touch a single partition.

## Q zh
在 2PL 和 SSI 之外，还有第三条通往 serializability 的路：真的把事务串行执行，在单线程上一次跑一个（VoltDB/H-Store；Redis 本质上也是这么工作的）。这为什么可行？必须满足哪三个条件？

## A zh
可行的原因在于：去掉并发就去掉了**全部**并发控制开销——没有锁、没有死锁、没有中止重试——而一个 CPU 核心在纯内存数据上顺序执行，远比直觉预期的要快；serializability 由构造直接保证。

条件：
- **数据必须装进内存**：任何一个事务碰到磁盘，都会卡住*唯一的*线程以及排在它后面的所有事务。
- **事务必须短小且非交互式**：整体一次性提交（存储过程），绝不在事务中途等待应用往返或用户输入——任何停顿都会阻塞整个世界。
- **吞吐必须塞进"每分区一个核"**：扩展方式是给数据分区、每个分区一个串行执行器；但**跨分区事务**需要在执行器之间协调，慢几个数量级——所以负载必须可分区，让绝大多数事务只碰单个分区。

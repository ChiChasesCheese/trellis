---
id: problems-stock-exchange-single-thread-vs-multithread-locking
node: problems.commerce.stock-exchange
type: qa
step: 3
tags: [grown]
---
## Q
Why would adding multiple threads to a single symbol's matching engine, protected by locks, actually be a worse design than keeping it single-threaded, given that the matching engine's whole job is to produce a deterministic, replayable order of matches?

## A
Multiple threads racing to acquire locks introduce a scheduling order that depends on OS thread scheduling and lock contention timing, which is not deterministic from one run to the next — the exact interleaving of operations can differ even given the identical set of input orders. This breaks the requirement that a replay of the same input sequence must always reproduce the same trade results, which is what durability and failover (replaying the journal on a replica) depend on. A single thread, by contrast, processes events strictly one at a time in the order it receives them, so the output is a pure function of the input sequence with no scheduling nondeterminism, and locking's cost (cache invalidation, contention) is avoided entirely.

## Q zh
撮合引擎的整个职责是产出一个确定性、可重放的成交顺序。既然如此，为什么给单支股票的撮合引擎加多线程（配合加锁保护）反而是比保持单线程更差的设计？

## A zh
多个线程争抢锁会引入一个依赖操作系统线程调度和锁竞争时机的执行顺序，这个顺序在不同运行之间不是确定性的——即使输入的订单集合完全相同，操作的具体交错顺序也可能不同。这违反了“重放同一份输入序列必须始终得到同一个成交结果”这条要求，而这正是持久化和故障转移（副本重放日志）赖以成立的前提。相比之下，单线程严格按照事件到达的顺序逐个处理，输出是输入序列的纯函数，不存在调度上的不确定性，同时也完全避免了加锁的代价（缓存失效、锁竞争）。

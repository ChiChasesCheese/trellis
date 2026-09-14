---
id: storage-inmemory-advantage
node: storage.internals.tradeoffs
type: qa
---
## Q
A disk database with its working set fully in OS page cache still loses to Redis. If not disk reads, what is the in-memory store's real advantage — and how does it get durability anyway?

## A
It skips the machinery of pretending memory is disk: no encoding rows into disk-page format, no buffer-pool management, and it can use structures impractical to serialize to disk — Redis's sorted sets, native lists, HyperLogLog. Plus a single-threaded event loop with no locking on the hot path.

Durability without losing the speed: writes are **appended to a log** (Redis AOF, `everysec` fsync by default) and/or periodic **snapshots** (RDB); recovery replays them. The dataset must fit in RAM — the log is for recovery, not for reads. Trade-off: `everysec` risks ~1s of writes on crash.

## Q zh
一个磁盘数据库的工作集完全在 OS 页缓存中仍然输给 Redis。如果不是磁盘读，内存存储的真实优势是什么——它如何获得持久性的呢？

## A zh
它跳过了假装内存是磁盘的机制：没有将行编码为磁盘页格式，没有缓冲池管理，并且它可以使用实际上无法序列化到磁盘的结构——Redis 的有序集、本地列表、HyperLogLog。加上单线程事件循环，热路径上无锁定。

没有失去速度的持久性：写被 **append 到日志**（Redis AOF，`everysec` fsync 默认）和/或周期性**快照**（RDB）；恢复重放它们。数据集必须在 RAM 中——日志是为了恢复，不是读。权衡：`everysec` 在崩溃时风险 ~1 秒的写。

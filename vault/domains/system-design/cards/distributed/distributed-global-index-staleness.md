---
id: distributed-global-index-staleness
node: distributed.partitioning.indexes
type: qa
---
## Q
A global (term-partitioned) secondary index is updated asynchronously. Name the two failure modes this creates for application logic, and the operational gotcha nobody expects.

## A
- **Read-your-writes is gone on the index path**: you write an item and immediately query the index — the item is missing (usually sub-second, but unbounded when the index is throttled or backlogged). Any UI that writes then re-queries by the indexed attribute will look broken.
- **Read-modify-write off the index is unsafe**: the index can return a *stale version* of an item, or an item that no longer matches the predicate. Treat a global index as a **lookup of candidate keys**, then re-read the base row for authoritative values before acting on it.

Operational gotcha: the index has **its own capacity**, and back-pressure flows backwards. In DynamoDB, if a GSI can't absorb the write rate, **writes to the base table are throttled** — an under-provisioned index takes down the table it was meant to accelerate. Also, a deleted/unmatched item requires a *delete* in the index partition, so backlogs surface as ghost entries, not just missing ones.

## Q zh
一个全局（按 term 分区的）二级索引是异步更新的。这给应用逻辑带来了哪两种失败模式？还有一个没人会预料到的运维陷阱是什么？

## A zh
- **索引路径上的 read-your-writes 没了**：你写入一条记录，立刻用索引去查——查不到（通常是亚秒级延迟，但当索引被限流或积压时可以无上限地长）。任何"写完立刻按被索引属性再查一次"的 UI 都会看起来像坏了。
- **脱离索引做 read-modify-write 是不安全的**：索引可能返回一条记录的*陈旧版本*，或者一条已经不再匹配该谓词的记录。要把全局索引当成一次**候选 key 的查找**，在据此采取行动之前，回到 base row 重新读取权威值。

运维陷阱：索引**有自己的容量**，而背压是反向传导的。在 DynamoDB 中，如果一个 GSI 吸收不了写入速率，**base table 上的写入也会被限流**——一个容量不足的索引会拖垮它本该加速的那张表。另外，一条被删除/不再匹配的记录需要在索引分区里执行一次*删除*，所以积压表现出来的不只是缺失的条目，还会有幽灵条目（ghost entries）。

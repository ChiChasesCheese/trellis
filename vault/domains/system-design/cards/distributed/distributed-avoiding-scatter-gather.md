---
id: distributed-avoiding-scatter-gather
node: distributed.partitioning.indexes
type: qa
---
## Q
You need a second access pattern on a sharded table and don't want scatter-gather. What are your options besides a built-in global index, and how do you choose?

## A
- **Query-shaped duplicate table** ("one table per query", Cassandra idiom): write the same fact twice, partitioned differently. You own the fanout on write and the consistency between copies; reads are single-partition and fast. Keep it correct with the **outbox/CDC pipeline**, not dual writes from app code.
- **Async materialized view from the change log**: consume CDC and build the derived table. Same result, one writer, replayable — and the lag is observable as consumer offset lag rather than invisible.
- **Composite key that serves both patterns**: partition by `hash(tenant)`, sort by `(status, created_at)` — a filter that's a prefix of the sort key needs no index at all.
- **Bound the fanout instead of removing it**: partition by a coarse bucket of the query attribute so a query touches 4 shards, not 400.

Choose by read/write ratio and staleness tolerance: read-heavy + tolerant of ~seconds of lag → derived table/view; write-heavy or must-be-consistent → local index and accept scatter-gather, or fix the partition key. Also check the **projection**: an index that doesn't carry the columns you select forces a second round trip to the base partition per matched item, which quietly reinstates the fanout.

## Q zh
你需要在一张分片表上支持第二种访问模式，又不想用 scatter-gather。除了内置的全局索引，你还有哪些选择？该怎么选？

## A zh
- **按查询形状复制的表**（"每个查询一张表"，Cassandra 的惯用法）：把同一份事实写两次，用不同的方式分片。你需要自己负责写入时的扇出以及两份副本之间的一致性；读取是单分区且快速的。用 **outbox/CDC 管道**来保证正确性，而不是应用代码里的双写。
- **基于变更日志的异步物化视图**：消费 CDC 并构建派生表。结果相同，但只有一个写者、可重放——延迟以消费者 offset lag 的形式可观测，而不是隐形的。
- **同时服务两种模式的复合键**：按 `hash(tenant)` 分区，按 `(status, created_at)` 排序——只要过滤条件是排序键的前缀，就完全不需要索引。
- **限制扇出而不是消除它**：按查询属性的粗粒度桶分区，让一次查询只打到 4 个分片，而不是 400 个。

按读写比和对陈旧数据的容忍度来选择：读多、能容忍几秒延迟 → 派生表/视图；写多或必须保持一致 → 本地索引并接受 scatter-gather，或者修正分区键。同时要检查**投影**：如果索引不携带你要 select 的列，每条匹配项都要多一次到基础分区的往返，这会悄悄地把扇出又带回来。

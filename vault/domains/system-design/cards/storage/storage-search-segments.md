---
id: storage-search-segments
node: storage.search
type: qa
---
## Q
Lucene segments are immutable. What do update and delete actually do, and what background process pays the bill?

## A
- **Delete**: the doc is only *marked* in a per-segment deletion bitmap; it still occupies space and is filtered out at query time.
- **Update**: delete-mark the old version + index a full new document into a fresh segment — there is no in-place field update.

**Segment merging** pays the bill: background merges combine small segments into larger ones, physically dropping deleted docs. It's Lucene's compaction — same trade as [[storage-amplification-triangle]]: merge I/O competes with queries, and an update-heavy index carries growing "deleted but not merged" overhead (watch `docs.deleted`). Per-query cost also scales with segment count, which is why merging matters for latency, not just space.

## Q zh
Lucene 分段是不可变的。更新和删除实际上做什么，什么后台进程付钱？

## A zh
- **删除**：文档仅在每分段删除位图中被**标记**；它仍占据空间，在查询时被过滤掉。
- **更新**：删除标记旧版本 + 在新分段中索引完整新文档——无原地字段更新。

**分段合并**付钱：后台合并把小分段合并成更大的，物理上丢弃被删除的文档。它是 Lucene 的压实——与 [[storage-amplification-triangle]] 相同权衡：合并 I/O 与查询竞争，更新-重索引携带增长的"已删除但未合并"开销（观看 `docs.deleted`）。每查询成本也按分段数缩放，这就是为什么合并对延迟重要，不只是空间。

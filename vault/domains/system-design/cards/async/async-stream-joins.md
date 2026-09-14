---
id: async-stream-joins
node: async.streaming.processing
type: qa
---
## Q
Stream-stream join vs stream-table join: how does each maintain state, and what goes wrong with each?

## A
- **Stream-stream** (clicks ⋈ impressions): both sides are buffered in a **windowed state store**; each arrival probes the other side's buffer. Failure mode: the window bounds the wait — a match arriving later than the window is silently a non-join, so window size trades completeness against state size.
- **Stream-table** (orders ⋈ customer profile): the table side is a **changelog materialized into a local store** (compacted topic → RocksDB); each event looks up current state. Failure mode: **time skew** — the event may join against a *newer* table version than existed at event time; versioned/temporal joins fix this at extra state cost.

Both require **co-partitioning**: same key, same partition count, or a repartition (shuffle) topic is inserted first.

## Q zh
Stream-stream join vs stream-table join：每个如何维护状态，每个出什么问题？

## A zh
- **Stream-stream**（clicks ⋈ impressions）：两边都在**windowed state store** 中缓冲；每个到达都探测另一边的缓冲区。故障模式：窗口限制等待 — 晚于窗口到达的匹配无声地是非 join，所以窗口大小权衡完整性对状态大小。
- **Stream-table**（orders ⋈ customer profile）：table 端是**changelog 物化到本地存储**（压缩 topic → RocksDB）；每个事件查询当前状态。故障模式：**时间偏差** — 事件可能对比事件时间存在的*更新的*表版本 join；版本化/时间 join 以额外状态代价修复。

两者都需要**共分区**：相同 key、相同 partition 数，或先插入 repartition（shuffle）topic。

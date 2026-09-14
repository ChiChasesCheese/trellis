---
id: async-log-compaction
node: async.log
type: qa
---
## Q
How does Kafka log compaction work, what does a compacted topic guarantee, and what is it for?

## A
A background cleaner rewrites old log segments, keeping **only the latest record per key**; a `null` value is a **tombstone** that marks the key for deletion (retained for a grace period so consumers see it before it vanishes). The active segment is never compacted, and offsets are preserved — they just become sparse.

Guarantee: a consumer reading from the beginning gets **at least the final state of every key** — a full snapshot plus recent history, in bounded space.

Use it for **changelog/state topics**: CDC feeds, materialized-view backing state (Kafka Streams), config/entity snapshots. Use time-based retention instead when you need *every* event, not just the last per key.

## Q zh
Kafka log compaction 如何工作，压缩后的 topic 保证什么，它用来做什么？

## A zh
后台 cleaner 重写旧日志 segment，**仅保留每个 key 的最新记录**；`null` 值是**墓碑**，标记该 key 待删除（保留一段时间，使 consumer 在它消失前能看到）。活跃 segment 永远不被压缩，offset 被保留 — 它们只是变得稀疏。

保证：从头读取的 consumer 得到**至少每个 key 的最终状态** — 完整快照加最近历史，空间有限。

用它来处理**changelog/state topic**：CDC 流、materialized-view 支持状态（Kafka Streams）、配置/实体快照。当你需要*每个*事件而不是每个 key 的最后一个时，改用基于时间的保留。

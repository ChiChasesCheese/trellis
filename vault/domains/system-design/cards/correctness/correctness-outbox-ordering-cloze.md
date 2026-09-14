---
id: correctness-outbox-ordering-cloze
node: correctness.outbox
type: cloze
---
To preserve event order through an outbox: the relay publishes rows in {{c1::commit/insert order (monotonic outbox sequence)}}, uses {{c2::the aggregate id (e.g. account id) as the broker partition key}} so one entity's events stay in one partition, and a polling relay must run {{c3::single-writer per partition/shard}} — parallel unordered pollers silently reorder events.

## zh
通过 outbox 保留事件顺序：relay 按 {{c1::提交/插入顺序（单调 outbox 序列）}}发布行，用 {{c2::聚合 id（如账户 id）作为 broker 分区 key}}，让一个实体的事件停留在一个分区，轮询 relay 必须运行 {{c3::单个写入器每分区/分片}} — 平行无序轮询器无声地乱序事件。

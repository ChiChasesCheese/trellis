---
id: async-compacted-topic-bootstrap
node: async.streaming.cdc
type: qa
---
## Q
Team A bootstraps every new CDC consumer with the snapshot-plus-log-position dance; team B just points new consumers at offset 0 of a compacted changelog topic. What lets team B skip the snapshot, and what two properties must their change events have?

## A
Log compaction keeps **at least the latest record per key** forever, so the compacted topic *is* a full copy of the current dataset plus recent history — reading it from offset 0 delivers a complete bootstrap, and the same subscription then continues seamlessly into live updates. No separate snapshot pipeline, no offset-stitching to get wrong, and it works for the tenth consumer as well as the first.

Required event properties:
- **Full-state records, keyed by primary key**: each event carries the row's entire new value ("after" image), not a diff — compaction throws away older events for the key, so a survivor must stand alone.
- **Deletes as tombstones**: a deletion must be written as a null-value record for the key; otherwise compacted history resurrects deleted rows for every future consumer.

Residual caveat: bootstrap time grows with keyspace size (you still read every live key), and until the read reaches the tail you're seeing a mixture of old and new — same idempotent-upsert discipline as any CDC consumer.

## Q zh
A 团队每接入一个新的 CDC 消费者，都要走一遍"快照 + 日志位点"的仪式；B 团队只是把新消费者指向一个 compacted changelog topic 的 offset 0。是什么让 B 团队可以跳过快照？他们的变更事件必须具备哪两个性质？

## A zh
日志压缩（log compaction）永久保留**每个 key 至少最新的一条记录**，所以压缩后的 topic *本身就是*当前数据集的完整拷贝加上近期历史——从 offset 0 读一遍就完成了完整引导，而且同一份订阅随后无缝衔接到实时更新。不需要单独的快照管线，没有可能搞错的位点缝合，第十个消费者和第一个一样好使。

事件必须具备的性质：
- **以主键为 key 的全量状态记录**：每个事件携带该行完整的新值（"after"镜像），而不是增量 diff——压缩会丢掉该 key 更早的事件，幸存的那条必须能独立成立。
- **删除写成 tombstone**：删除必须写成该 key 的空值（null）记录；否则压缩后的历史会让已删除的行在每个未来消费者面前复活。

残余注意点：引导时间随 key 空间增长（活着的 key 都要读一遍），而且在读到尾部之前你看到的是新旧混合状态——和任何 CDC 消费者一样，要守幂等 upsert 的纪律。

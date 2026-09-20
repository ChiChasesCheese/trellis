---
id: problems-message-queue-log-compaction-vs-time-retention
node: problems.foundations.message-queue
type: qa
step: 6
tags: [grown]
---
## Q
In a Kafka-class message queue, why would applying the same time/size-based retention policy (delete whole segments older than N days) to a topic used as the authoritative store of each key's current state (rather than a pure event stream) cause data loss, and what alternative cleanup policy fixes it?

## A
Time/size-based deletion removes entire log segments once they age past the retention window, regardless of whether a given key's most recent (and still valid) value happens to live in that old segment -- a key that was last updated 8 days ago on a 7-day retention topic would simply disappear, even though its value is still current. Log compaction (cleanup.policy=compact) fixes this by having a background log cleaner rewrite each partition keeping only the latest record per key (tracked via a per-partition hash table of key to last offset), discarding earlier values for the same key but never discarding a key's current value purely due to age; a null-payload tombstone record marks a key as deleted until the tombstone itself is later cleaned up.

## Q zh
在一个 Kafka 一类消息队列里，如果把同样的按时间/大小保留策略（删除超过 N 天的整个 segment）用在一个作为「每个 key 当前状态」权威存储的主题上（而不是纯事件流），为什么会导致数据丢失？什么样的替代清理策略能修复这个问题？

## A zh
按时间/大小删除是整段整段地删除超出保留窗口的 log segment，完全不管某个 key 最新（依然有效）的那条记录是不是恰好落在这个旧 segment 里——在一个保留期 7 天的主题上，一个 8 天前才最后更新过的 key 会直接消失，即使它的值依然是当前有效的。日志压缩（log compaction，cleanup.policy=compact）解决了这个问题：后台的 log cleaner 进程重写每个分区，只保留每个 key 最新的一条记录（通过一张按分区维护的「key 到最后 offset」哈希表跟踪），丢弃同一 key 更早的旧值，但绝不会仅仅因为太旧就丢弃一个 key 当前有效的值；一条 value 为空的墓碑（tombstone）记录用来标记某个 key 已被删除，直到墓碑本身之后被清理。

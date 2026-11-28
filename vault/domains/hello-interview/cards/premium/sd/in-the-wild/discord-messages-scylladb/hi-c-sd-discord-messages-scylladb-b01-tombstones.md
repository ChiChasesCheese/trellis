---
id: hi-c-sd-discord-messages-scylladb-b01-tombstones
node: sd.in-the-wild.discord-messages-scylladb.beyond
type: qa
step: 1
---
## Q
**Discord 消息存储 · Cassandra 删除与墓碑**｜拓展 · 加分

消息可以被删除。Cassandra 里删除一条消息为什么会变成读性能问题？

## A
- **删除不是真删：** 因为 SSTable 不可变，删除写入的是一条墓碑（tombstone）标记，表示"这条已删除"；真正的数据在压实时才被清理，而且墓碑要保留一段时间（`gc_grace_seconds`，默认 10 天），确保所有副本都收到删除。
- **读的代价：** 读一个分区时，要扫过其中的墓碑才能找到存活的行；大量删除的分区会让读变慢，甚至触发墓碑过多的告警或失败。
- **与本案例的关系：** 压实积压会让墓碑清得更慢，读更慢，是同一个恶性循环的一部分。
- **面试用法：** 说到 Cassandra 就要提：追加式存储带来写便宜，但更新与删除的代价延后到读和压实，模型不适合"频繁删除、频繁覆盖"的负载。

---
id: hi-sd-cassandra-7-discord-case
node: qb.sd.notification-system-scale.pre-sd-deep-dives-cassandra
type: qa
step: 7
---
## Q
**案例：Discord 消息表如何防止大分区**｜系统设计 · 深入专题

Discord 用 Cassandra 存聊天消息，最初的主键是什么？遇到什么问题？后来怎么改？

## A
**要点。** 访问模式：多数人读频道最近的消息，并向上滚动，所以要倒序。

初版：`PRIMARY KEY (channel_id, message_id)`，`message_id DESC`。一个频道的消息落在同一分区，无需散播汇聚。用 Snowflake ID（按时间可排序且不冲突的 ID）而不是 `created_at`，因为毫秒时间戳仍可能冲突。

**问题。** 繁忙频道的分区太大，Cassandra 对大分区吃力；而且频道只增不减，早晚会撑爆。

**改法。** 把时间桶（bucket）加进分区键：`PRIMARY KEY ((channel_id, bucket), message_id)`，一个桶是固定的 10 天窗口（以 2015-01-01 为起点）。10 天内最忙的频道也装得下一个分区，分区不再无限增长；最新消息通常在同一个桶里，所以多数读写只查一个分区。

**例外。** 桶刚切换的时刻，或不活跃的频道（少数查询），才需要跨桶读取。

- **2026 亮点：** Discord 后来又把这套消息存储从 Cassandra 换成了 ScyllaDB：C++ 实现没有 JVM 垃圾回收停顿，节点数减少一半以上，尾延迟明显下降；并在存储前加了一层按频道合并请求的数据服务，挡住热门频道的突发读。面试里可以拿来说明：数据模型选对之后，剩下的瓶颈往往在运维和实现层面。

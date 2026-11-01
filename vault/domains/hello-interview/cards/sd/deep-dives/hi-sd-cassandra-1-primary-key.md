---
id: hi-sd-cassandra-1-primary-key
node: qb.sd.notification-system-scale.pre-sd-deep-dives-cassandra
type: qa
step: 1
---
## Q
**数据模型与主键：分区键加聚簇键**｜系统设计 · 深入专题

Cassandra 的主键由什么构成？分区键（partition key）和聚簇键（clustering key）分别决定什么？

## A
**要点。** 主键 = 分区键（一列或多列）+ 可选的聚簇键。

- 分区键：对它做哈希，决定这一行落在哪个分区、哪些节点上。
- 聚簇键：决定同一分区内各行的排序，需要按时间倒序、按楼层排序时就靠它。

```sql
-- 分区键 (channel_id, bucket)，聚簇键 message_id 倒序
PRIMARY KEY ((channel_id, bucket), message_id)
  WITH CLUSTERING ORDER BY (message_id DESC)
```

**背景。** Cassandra 是宽列（wide-column）库：同一张表里每行可以有不同的列，不必为空列填 NULL；每一列都带写入时间戳，副本冲突时「最后写入者胜」（last write wins）。键结构与 DynamoDB 的分区键、排序键基本一一对应。

**易错。** 双括号 `((a, b), c)` 是复合分区键；`(a, b, c)` 是 a 为分区键，b、c 为聚簇键。别写混。

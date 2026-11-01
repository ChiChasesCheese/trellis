---
id: hi-sd-top-k-2-baseline
node: sd.problem-breakdowns.top-k
type: qa
step: 2
---
## Q
**起步方案：Kafka、Postgres 和索引**｜系统设计 · 题目拆解

YouTube Top K 先要一个能跑通的基础版本。播放事件来自一个按视频 ID 分区的 Kafka 流，请说明怎样先支持“全部时间 Top K”，再扩展到按小时、天、月的窗口，各自的代价在哪。

## A
**要点。** 消费者读取播放事件，把对应视频的计数加一，写进 Postgres；在 views 列上建索引，查询 `ORDER BY views DESC LIMIT k` 沿着有序索引取前 K 条，近似 O(k)。

**窗口扩展。** 表里加一个“小时级时间戳”列，每个视频每小时一行。查询变成按视频做 `SUM(views)` 再排序，窗口越大要扫描的行越多，成了全表级聚合，这是后面所有深挖的起点。

**代价。** 写入从追加的 O(1) 变成维护索引的 O(log n)；单个 Postgres 要吃下全部写入，明显撑不住。

**易错。** 起步时先说出这些瓶颈再继续，让面试官知道你是故意先做简单版，不是漏看。

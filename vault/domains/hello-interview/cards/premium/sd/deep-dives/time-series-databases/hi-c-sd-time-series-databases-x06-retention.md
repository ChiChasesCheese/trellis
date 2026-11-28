---
id: hi-c-sd-time-series-databases-x06-retention
node: sd.deep-dives.time-series-databases.exam
type: qa
step: 6
---
## Q
**时序数据库 · 保留期实现**｜考点 · 必会

要求只保留 90 天监控数据。比较「Postgres 大表加 `DELETE WHERE ts < now()-90d`」与「按天分区、删旧分区」，各有什么问题？

## A
- **大表 DELETE：** 要扫描并逐行标记删除，产生大量写和日志，在 Postgres 里还留下死元组，要靠 vacuum 回收；删除期间影响正常读写，磁盘空间也不会马上还。
- **按天分区：** 90 天前的整个分区直接删文件（或 `DROP` 分区），是元数据操作，代价与数据量无关，几乎不影响线上。
- **其他收益：** 查询天然只碰相关分区；写只进当天分区。
- **要点：** 分区边界要与保留期对齐；分区粒度太细会产生大量小文件，太粗则删得不及时。

---
id: hi-pt-stock-price-alerts-8-db-choice
node: qb.sd.stock-price-alerts.points
type: qa
step: 8
---
## Q
**股票价格提醒系统 · 数据库怎么选**｜出自：股票价格提醒系统 › 深入 4

股价提醒系统的判断路径不依赖数据库，那么订阅和规则的数据库怎么选？

## A
**需求。** 规则变更不频繁，数据量 2 GB 到十几 GB，需要按用户和按股票两个方向查询。
**关系库。** PostgreSQL 事务简单，订阅表加用户、股票两个索引，分片后够用，便于管理统计。
**键值或宽列。** DynamoDB、Cassandra 以 symbol 为分区键、阈值#user_id 为排序键，适合判断节点按股票批量加载，按用户查询建二级索引。
**要点。** 低延迟来自内存结构，不是数据库。

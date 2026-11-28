---
id: hi-pt-typeahead-search-system-6-pipeline
node: qb.sd.typeahead-search-system.points
type: qa
step: 6
---
## Q
**搜索联想 · 数据管线**｜必会 · 出自：搜索联想 › 深入 3

联想的基础数据怎样从搜索日志变成线上可查的快照？

## A
**流程。** 搜索日志（Kafka）→ 批处理（每小时或每天）统计每个查询的衰减热度 → 过滤（次数低于阈值、含敏感词、疑似个人信息的丢弃）→ 为每个前缀选前 10 → 写出新快照文件 → 联想服务下载后原子切换指针；失败就保留旧版本。

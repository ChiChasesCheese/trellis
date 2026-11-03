---
id: hi-sd-ad-click-aggregator-4-olap-vs-tsdb
node: sd.problem-breakdowns.ad-click-aggregator.exam
type: qa
step: 4
---
## Q
**分析库选型：OLAP 还是时序库**｜系统设计 · 问题拆解

预聚合结果该放在什么数据库里？为什么选 OLAP（Redshift、Snowflake、BigQuery）而不是时序数据库（InfluxDB、TimescaleDB）？

## A
**要点。** OLAP 数据库采用列式存储，对数百万行做 COUNT、SUM、AVG 这类聚合，比行存数据库快得多，适合分析查询。

**取舍。** 时序库（TSDB）擅长「某个指标在时间范围内的值」，且基数较低。这里有数百万个广告 ID，广告主之后还会想按设备、地域、广告系列等多个维度切片，高基数、多维的查询用 OLAP 更合适。

**易错。** 如果面试官的要求只是对单一指标做简单的时间范围查询，提出时序库也完全合理，但要准备好讲取舍。

**使用时机。** 分析型存储在这里看的是：聚合速度、维度灵活性，而不是写入速度。写入速度由前面的事件流和预聚合负责。

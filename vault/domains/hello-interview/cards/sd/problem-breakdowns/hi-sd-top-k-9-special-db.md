---
id: hi-sd-top-k-9-special-db
node: sd.problem-breakdowns.top-k
type: qa
step: 9
---
## Q
**专用数据库是否适合 Top K**｜系统设计 · 题目拆解

面对 YouTube Top K，面试官问能否用时序数据库或实时 OLAP 数据库。请评价 InfluxDB / Prometheus、TimescaleDB、Druid / Pinot / ClickHouse 的适配度，并说明面试里应该怎样对待它们。

## A
**InfluxDB / Prometheus（不适合）。** 它们擅长查单条序列，视频 ID 当标签会有数十亿个序列，要跨所有序列取前 K，等于全库扫描，基数太高撑不住。

**TimescaleDB（可以）。** 本质是带时间分区（hypertable）的 Postgres。按小时的单窗口能走索引；跨多个小时要用连续聚合（continuous aggregate）维护近一小时 / 一天 / 一月的汇总表并在 views 上建索引。它和前面自建的“每窗口一张表”几乎一样，仍然需要缓存和分片。

**Druid / Pinot / ClickHouse（可以）。** 都在写入时预聚合：Druid 做 rollup，Pinot 用 star-tree，ClickHouse 用物化视图加 SummingMergeTree。线上节点故障和合并会影响延迟。

**取舍。** 面试官会追问内部机制，别靠背技术名字；先用基本组件推出数据流，再说明专用库为什么合适。

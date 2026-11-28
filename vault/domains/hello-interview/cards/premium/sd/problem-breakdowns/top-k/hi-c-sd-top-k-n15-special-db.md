---
id: hi-c-sd-top-k-n15-special-db
node: sd.problem-breakdowns.top-k.notes
type: qa
step: 15
---
## Q
**Top K · 深入六：时序库和实时 OLAP 库值得用吗**｜摘要 · 追问

面试官问能不能用时序数据库或实时 OLAP 数据库做 Top K。几类产品各自适不适合，面试里该怎样对待？

## A
- **核心矛盾：** 视频 ID 有数十亿个，高基数（cardinality，不同取值的个数）是这个问题的主要难点，靠预计算和缓存解决，与选哪种数据库关系不大。
- **InfluxDB、Prometheus（不适合）：** 擅长取单个序列的曲线，把视频 ID 当标签就有数十亿条序列；要跨所有序列取前 K，等于全库扫描。
- **TimescaleDB（可以）：** 带时间分区（hypertable）的 Postgres。单个小时可以走 views 索引做 O(k)；跨多个小时无法用索引合并，要用连续聚合（continuous aggregate）维护近一小时、一天、一月的汇总表并在 views 上建索引。本质上就是自建的"每窗口一张表"，仍要缓存和分片。
- **实时 OLAP**（Druid、Pinot、ClickHouse，可以）： 都在写入时预聚合：Druid 按时间桶加视频做 rollup，Pinot 靠 star-tree 索引，ClickHouse 靠物化视图加 SummingMergeTree。线上节点故障、合并压缩会影响延迟，需要深入了解机理。
- **面试策略：** 先用基本组件推导出数据流，再说明专用库为什么对应这种数据流；背产品名不如理解它为什么出现，面试官会追问内部机制。

---
id: hi-sd-ad-click-aggregator-6-scale-writes
node: sd.problem-breakdowns.ad-click-aggregator
type: qa
step: 6
---
## Q
**扩展到每秒 1 万次点击**｜系统设计 · 问题拆解

流水线每一环在 1 万次点击/秒下怎样扩展？Kinesis 的分片上限是多少，分区键为什么选广告 ID？

## A
**要点。**
- 点击处理服务：无状态，水平扩展，前面放负载均衡，托管云服务可按 CPU 或内存自动伸缩。
- 流：Kafka、Kinesis 本身是分布式的，但要配置好。Kinesis 每个分片上限是 1 MB/s 或 1000 条/s，所以要分片。按广告 ID 分区，同一广告的事件在同一分片，不同分片相互独立，可以并行读取。
- 流处理器：每个分片起一个 Flink 作业，负责该分片里的广告。
- OLAP 库：Snowflake、BigQuery 这类托管仓库自动扩展；自己部署的 ClickHouse 则按广告主 ID 分片，让同一广告主的数据在一个节点上，加速「看自己所有广告」的查询。

**易错。** 分区键的选择要同时顾及写入并行度（广告 ID）和查询局部性（广告主 ID），两者可以在不同层使用不同的键。别忘了监控查询性能是否满足 SLA。

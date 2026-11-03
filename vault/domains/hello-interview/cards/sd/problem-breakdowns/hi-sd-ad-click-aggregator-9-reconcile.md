---
id: hi-sd-ad-click-aggregator-9-reconcile
node: sd.problem-breakdowns.ad-click-aggregator.exam
type: qa
step: 9
---
## Q
**对账与 Lambda 架构**｜系统设计 · 问题拆解

流处理可能因处理错误、坏版本发布、乱序等产生细微误差。怎样兼顾低延迟和准确？这种架构叫什么？

## A
**要点。** 在流的末端，除了流处理器，还把原始点击事件持续落到数据湖（S3）：Kafka 用 S3 Sink Connector，Kinesis 用 Firehose，不会增加 Flink 的负载。再定期（每小时或每天）用 Spark 批处理读取原始事件重新聚合，与流处理的结果比较；不一致就查根因，并用正确值覆盖 OLAP 库。

**为什么。** 点击丢了就是丢钱，而正确性与低延迟常常互相冲突。对账让「快」由流处理负责，「准」由批处理兜底。

**取舍。** 这就是 Lambda 架构：速度层（Flink）给低延迟结果，批处理层（Spark）作为事实来源，定期纠正速度层的偏差。代价是维护两套计算逻辑。

**易错。** 对账不能替代实时路径：它只修正已发生的误差，不能让用户立即看到准确值。

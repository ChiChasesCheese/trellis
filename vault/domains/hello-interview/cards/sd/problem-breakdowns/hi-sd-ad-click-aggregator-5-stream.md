---
id: hi-sd-ad-click-aggregator-5-stream
node: sd.problem-breakdowns.ad-click-aggregator.exam
type: qa
step: 5
---
## Q
**用流处理做近实时聚合**｜系统设计 · 问题拆解

批处理有延迟。改成流处理时，点击到查询的链路怎么设计？为什么要用 Flink 而不是自己写 Kafka 消费者在内存里计数？

## A
**要点。** 点击处理服务把事件立即写入 Kafka 或 Kinesis；Flink（或 Spark Streaming）读取流，在内存里按广告 ID 和分钟窗口累加，窗口结束后写入 OLAP 库，广告主随即可查询。

**为什么用 Flink。** 自己写消费者定时刷库，中级面试尚可接受。Flink 额外提供：按事件时间（event time）开窗，乱序事件仍落入正确的分钟桶；水位线（watermark）判断何时可关闭窗口并处理迟到数据；exactly-once 保证；以及内置的状态恢复。这些自己实现容易出错。

**取舍。** 若窗口都是 1 分钟，流处理的端到端延迟和每分钟跑一次 Spark 差不多。但流处理有调节余地：可以缩短窗口，或者按分钟聚合、每隔几秒刷新一次，最新这一分钟的数据在分钟结束前不完整，属于预期。Spark 作业有启动开销，很难跑到几秒一次。

**要点。** 这是典型的「扩展写」（Scaling Writes）模式。

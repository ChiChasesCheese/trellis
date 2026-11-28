---
id: hi-c-sd-flink-n03-source-sink
node: sd.deep-dives.flink.notes
type: qa
step: 3
---
## Q
**Flink · 源与汇**｜摘要 · 必会

Flink 常见的源和汇有哪些？面试里为什么几乎总是从 Kafka 开始？

## A
- **源（source）：** 从外部系统读入并转成 Flink 流，常见 Kafka、Kinesis、文件系统、自定义源。
- **汇（sink）：** 把结果写出，常见数据库（MySQL、PostgreSQL、MongoDB）、数仓（Snowflake、BigQuery、Redshift）、消息队列（Kafka、RabbitMQ）、文件系统（HDFS、S3）。
- **为什么是 Kafka：** 绝大多数面试设计都从 Kafka 开始，它本来就逼你思考数据如何分到主题和分区，这和推理 Flink 作业的并行度直接相关。
- **别用来做批处理：** 技术上能做，但面试官不熟，也难以保持最优；批处理场景直接说 Spark。

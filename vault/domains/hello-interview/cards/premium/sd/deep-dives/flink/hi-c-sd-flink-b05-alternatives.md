---
id: hi-c-sd-flink-b05-alternatives
node: sd.deep-dives.flink.beyond
type: qa
step: 5
---
## Q
**Flink · Flink、Kafka Streams、Spark 的取舍**｜拓展 · 加分

有状态流处理除了 Flink 还有哪些选择？怎么挑？

## A
- **Kafka Streams：** 是嵌进应用里的库，不需要独立集群；状态存本地 RocksDB，并用 Kafka 的变更日志主题备份，只能读写 Kafka。适合逻辑不复杂、已经是 Kafka 技术栈、想少运维一套集群的团队。
- **Spark 默认微批：** Spark Structured Streaming 默认是微批（把流切成小批处理），吞吐高、与批处理共用代码和生态，延迟通常在秒级；对真正的毫秒级逐条处理不如 Flink。
- **Flink：** 逐条处理、事件时间和状态支持最成熟，延迟低，源汇丰富；代价是自己运维一个集群。
- **选择：** 逻辑简单且在 Kafka 内选 Kafka Streams；已有 Spark 平台且延迟要求宽松选 Spark；复杂状态、事件时间、低延迟选 Flink；托管版（如云上的 Flink 服务）能减轻运维。

---
id: async-broker-selection
node: async.queues
type: qa
---
## Q
Kafka vs RabbitMQ vs Pulsar: which workload picks which, and why?

## A
- **RabbitMQ (queue semantics)**: task distribution — per-message ack, redelivery to any consumer, routing/priority/delay features, consumer count not tied to partitions. Weak at replay and huge retention.
- **Kafka (log semantics)**: event streams shared by many consumers, replay, high-throughput ordered-per-key feeds. Parallelism is capped by partitions and per-message routing/priorities don't exist.
- **Pulsar**: both semantics on one cluster — segmented storage (BookKeeper) separates compute from storage, so topics scale without repartitioning and tiered offload is native; also strong multi-tenancy/geo-replication. Cost: more moving parts, smaller ecosystem.

Rule of thumb: *tasks* → queue semantics; *facts other systems will re-read* → log semantics ([[async-log-vs-queue]]).

## Q zh
Kafka vs RabbitMQ vs Pulsar: 哪种工作负载选择哪个，为什么？

## A zh
- **RabbitMQ（queue semantics）**：任务分发 — per-message ack、可重新投递给任意 consumer、支持 routing/priority/delay 特性、consumer 数量与 partition 无关。在 replay 和大规模保留方面较弱。
- **Kafka（log semantics）**：多个 consumer 共享的事件流、支持 replay、高吞吐量的 ordered-per-key 流。并行度受 partition 数量限制，不支持 per-message routing/priorities。
- **Pulsar**：单个集群上同时支持两种语义 — segmented storage（BookKeeper）将计算与存储分离，所以 topic 无需 repartitioning 就能扩容，tiered offload 原生支持；同时支持强多租户能力和地理复制。代价是系统复杂度高、生态相对较小。

经验法则：*任务* → queue semantics；*其他系统会重复读取的数据* → log semantics。

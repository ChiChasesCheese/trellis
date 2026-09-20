---
id: kafka-core-scalability-no-downtime
node: core.pubsub-why
type: qa
step: 6
source: kafka-2e
---
## Q
为什么说 Kafka 从一开始就被设计成「可以从单个 broker 平滑扩展到上百个 broker 的集群」？这种扩容会影响正在运行的集群吗？

## A
Kafka 的伸缩性（scalability）体现在：开发阶段可以只用单个 broker（一台 Kafka 服务器），随着数据量增长逐步扩展到包含上百个 broker 的生产集群，扩容过程不影响整体可用性——即使集群中个别 broker 失效，其余 broker（在配置了足够复制系数的前提下）仍能继续为客户端提供服务。这让 Kafka 既能满足小规模验证需求，也能承载大规模生产流量而不需要更换架构。

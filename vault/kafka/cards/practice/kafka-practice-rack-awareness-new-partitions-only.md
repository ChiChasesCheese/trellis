---
id: kafka-practice-rack-awareness-new-partitions-only
node: practice.sizing-tuning
type: qa
source: kafka-2e
---
## Q
给 broker 配置 `broker.rack` 参数启用「机架感知」（rack awareness）后，Kafka 会确保新分区的各个副本不会全部落在同一个机架上。但如果之后又对已有分区做了分区重分配（partition reassignment），机架感知的保证还能持续维持吗？

## A
不能自动维持。`broker.rack` 只影响**新创建**的分区在分配副本时的机架分布，Kafka 集群本身不会持续监控现有分区是否仍然满足机架感知（比如某次分区重分配之后，副本可能被意外集中到了同一个机架），也不会自动纠正这种情况。因此要长期维持机架感知带来的容灾效果（避免整个机架断电或故障时一个分区的全部副本同时不可用），需要引入外部的集群均衡工具持续检查和调整分区分布，而不能仅凭一次性配置 `broker.rack` 就一劳永逸。

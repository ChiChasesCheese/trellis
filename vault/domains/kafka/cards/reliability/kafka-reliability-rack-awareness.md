---
id: kafka-reliability-rack-awareness
node: reliability.broker-config
type: qa
step: 2
source: kafka-2e
---
## Q
Kafka 保证一个分区的多个副本会分布在不同的 broker 上，但为什么还建议额外配置 `broker.rack`（机架/可用区标识）？只保证「不同 broker」为什么不够？

## A
如果一个分区的所有副本恰好落在同一个机架里的不同 broker 上，那么只要这个机架的交换机发生故障，这些 broker 就会同时不可达，不管复制系数设得多高，这个分区照样整体不可用——「分散到不同 broker」防不住「整机架一起挂」这种相关性故障。配置 `broker.rack` 告诉 Kafka 每个 broker 所在的机架（在云上可以把可用区当机架用），Kafka 就会保证同一分区的副本分布在多个不同机架，这样单个机架或可用区故障时其余机架上的副本仍能维持分区可用。

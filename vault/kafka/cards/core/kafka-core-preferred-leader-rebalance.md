---
id: kafka-core-preferred-leader-rebalance
node: core.replication-isr
type: qa
source: kafka-2e
---
## Q
每个分区除了「当前首领」，还有一个「首选首领」（preferred leader）的概念，这是什么？为什么 Kafka 默认会定期把首领切回首选首领？

## A
首选首领是创建主题时按均衡原则选定的那个副本，也就是分区最初分配到的、能让各个 broker 承担的首领数量大致均衡的副本。如果之后发生过故障转移，当前首领可能变成了别的副本，导致某些 broker 承担过多首领职责、负载不均衡。auto.leader.rebalance.enable 默认为 true 时，Kafka 会定期检查首选首领是否同步且未担任当前首领，若满足条件就触发一次首领选举，把首领职责换回首选首领，从而让集群负载重新均衡。

---
id: kafka-internals-preferred-leader-rebalance
node: internals.replication-protocol
type: qa
step: 4
source: kafka-2e
---
## Q
Kafka 中的「首选首领（preferred leader）」是什么，为什么 Kafka 会在集群运行一段时间后自动把首领「换回」首选首领，而不是让当前首领一直当下去？

## A
首选首领是主题创建时，为每个分区在副本列表中排在第一位的那个副本；因为创建分区时 Kafka 会把各分区的首领尽量均匀地分散到不同 broker 上，首选首领天然对应着这种均衡分布。但集群运行中会发生 broker 下线导致首领切换到其它副本，切换久了负载就会往少数 broker 集中。当配置 `auto.leader.rebalance.enable`（默认为 true）打开时，Kafka 会定期检查：如果首选首领仍然是同步副本但已经不是当前首领，就触发一次首领选举把首领换回首选首领，从而把负载重新拉回原本设计的均衡状态。

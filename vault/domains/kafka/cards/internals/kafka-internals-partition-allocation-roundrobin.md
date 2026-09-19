---
id: kafka-internals-partition-allocation-roundrobin
node: internals.storage-segments
type: qa
step: 2
source: kafka-2e
---
## Q
Kafka 具体是怎样把一个分区的首领副本和跟随者副本分配到不同 broker 上的？在没有配置机架信息，和配置了机架信息两种情况下有什么区别？

## A
没有机架信息时：先随机挑一个起始 broker，然后用轮询（round robin）方式依次把各分区的首领副本分配给 broker 列表中的下一个 broker；对每个分区，再从它的首领所在 broker 开始，按 broker 编号顺序依次分配跟随者副本。配置了机架信息（Kafka 0.10.0 起支持）时，broker 列表不再按编号顺序轮询，而是按「机架交替」的顺序排列（例如两个机架各两台 broker 时排成 0、2、1、3），这样轮询分配出来的相邻副本总落在不同机架上，从而保证一个机架离线时分区仍有副本存活。

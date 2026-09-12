---
id: kafka-admin-preferred-vs-unclean-leader-election
node: admin.partition-reassignment
type: qa
source: kafka-2e
---
## Q
Kafka 支持「首选首领选举（preferred leader election）」和「不彻底的首领选举（unclean leader election）」两种首领选举方式，它们分别用来解决什么问题？为什么不彻底的首领选举有风险？

## A
每个分区的副本清单里，排在最前面的那个副本被指定为「首选首领」；正常情况下首领可能因为 broker 重启等原因转移给了别的副本，首选首领选举是把首领**换回**这个首选副本，目的是让各 broker 上的首领数量重新变得均衡，属于轻量、低风险操作，一般不会造成负面影响。不彻底的首领选举则用在极端情况：某个分区的首领副本不可用，且其余副本都不在 ISR（同步副本集合）里、按规则没资格当首领，导致这个分区彻底不可写不可读；这时候强行选一个非 ISR 副本当首领，能让分区恢复可用，但代价是所有已经写到旧首领、还没同步到这个副本的消息都会丢失，所以只应在能接受数据丢失或必须尽快恢复可用性时使用。

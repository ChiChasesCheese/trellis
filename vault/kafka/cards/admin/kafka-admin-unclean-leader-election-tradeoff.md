---
id: kafka-admin-unclean-leader-election-tradeoff
node: admin.dynamic-config
type: qa
source: kafka-2e
---
## Q
broker 的动态配置参数 `unclean.leader.election.enable` 允许一个没有跟上首领进度的副本（不在 ISR 里）被选为新首领，这本质上是拿什么去换取什么？什么场景下适合临时开启？

## A
这个参数是用「可能丢失部分尚未同步到该副本的数据」去换取「集群能更快恢复可用性」：正常情况下 Kafka 只允许在 ISR（同步副本集合）内选举新首领以保证不丢数据，但如果 ISR 中的副本全部不可用，分区就会一直处于离线、不可写状态。当业务能够接受这段时间的数据丢失，或者集群已经发生了不可恢复的数据丢失、必须尽快让分区重新可用时，可以短暂打开这个开关，让一个非 ISR 副本也能当选首领，尽快恢复读写；这不应作为长期开启的默认设置。

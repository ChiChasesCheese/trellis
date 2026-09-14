---
id: kafka-core-isr-leader-election-eligibility
node: core.replication-isr
type: qa
source: kafka-2e
---
## Q
首领所在的 broker 突然崩溃，Kafka 会从哪些副本里选出新首领？为什么一个长期落后的跟随者副本不能被选为新首领？

## A
Kafka 只会从 ISR（同步副本集合）里的副本中选举新首领，因为只有同步副本才能保证已经拥有首领此前确认过的全部消息。一个长期落后、不在 ISR 内的跟随者副本数据落后于首领，如果被选为新首领会导致部分已确认的消息「消失」，所以这类不同步副本没有资格参选，必须先追上首领、重新进入 ISR 才行。

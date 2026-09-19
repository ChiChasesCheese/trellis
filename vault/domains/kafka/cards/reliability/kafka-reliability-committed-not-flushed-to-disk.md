---
id: kafka-reliability-committed-not-flushed-to-disk
node: reliability.guarantees
type: qa
step: 3
source: kafka-2e
---
## Q
Kafka 判定一条消息「已提交」的标准，是要求它被写到磁盘上吗？如果不是，判定标准是什么？

## A
不是。Kafka 认为消息「已提交」的条件是它已经被写入该分区**全部同步副本（ISR）**，而不要求这些副本已经把数据从操作系统缓存冲刷（flush）到磁盘上——落不落盘是操作系统按自己的策略决定的时机问题，Kafka 主要靠多副本复制而不是靠强制刷盘来保证持久性。生产者可以通过 `acks` 配置选择自己关心的确认级别：只要求消息发到网络上、只要求首领副本写入，或者要求所有同步副本都确认写入。

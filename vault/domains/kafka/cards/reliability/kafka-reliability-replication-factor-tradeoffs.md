---
id: kafka-reliability-replication-factor-tradeoffs
node: reliability.broker-config
type: qa
source: kafka-2e
---
## Q
把一个主题的复制系数（replication factor，参数 `replication.factor`）从 3 提到 5，能多容忍几个 broker 同时失效仍可读写？这个提升是「免费」的吗，会带来哪些额外代价？

## A
复制系数为 *N* 时，最多可以容忍 *N*-1 个 broker 失效而分区仍可读写；从 3 提到 5，能多容忍 2 个 broker 同时失效（从容忍 2 个提升到容忍 4 个）。但这不是免费的：1）需要至少 *N* 个 broker，且每份数据占用 *N* 倍磁盘空间——本质是用硬件换可用性；2）每增加一个副本都会增加 broker 间的复制流量，例如以 10 MBps 写入时，2 副本多 10 MBps 复制流量，3 副本多 20 MBps，5 副本多 40 MBps，需要计入集群容量规划；3）由于每条消息要复制到全部同步副本才能被消费者读到，理论上副本越多，出现复制滞后拖慢端到端延迟的概率越大。

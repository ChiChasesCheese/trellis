---
id: kafka-internals-isr-matters-leader-election
node: internals.replication-protocol
type: qa
step: 3
source: kafka-2e
---
## Q
为什么「一个副本是否在 ISR（in-sync replicas，同步副本集合）里」这件事，会直接决定首领（leader）故障时谁能接任新首领？

## A
只有持续、及时地向首领发送 `Fetch` 请求并追上最新消息的「同步副本」才会被算进 ISR；不同步的副本意味着它没有拿到首领已经确认写入的全部消息。如果首领崩溃，Kafka 只允许从 ISR 中选出新首领，因为只有 ISR 里的副本才能保证不丢失任何已经写入首领的数据；如果允许一个滞后的副本当选，新首领会缺失部分消息，破坏「已提交消息不丢」的承诺。

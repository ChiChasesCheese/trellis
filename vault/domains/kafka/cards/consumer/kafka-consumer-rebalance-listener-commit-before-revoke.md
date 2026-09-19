---
id: kafka-consumer-rebalance-listener-commit-before-revoke
node: consumer.groups-rebalance
type: qa
step: 5
source: kafka-2e
---
## Q
消费者即将因为再均衡而失去某个分区的所有权之前，为什么最好在 `onPartitionsRevoked()` 回调里主动提交偏移量，而不是等下一次常规的自动/手动提交？

## A
`onPartitionsRevoked()` 会在消费者真正放弃分区所有权之前被调用，这是提交该分区最后处理进度的最后机会：一旦所有权转移给了群组里的其他消费者，新的所有者会从上一次提交的偏移量开始读取。如果没有在放弃所有权之前及时提交，新消费者可能会从一个更旧的偏移量重新开始，导致部分消息被重复处理；因此把提交偏移量的逻辑放在这个回调里，可以保证分区易主时读取进度不丢失、不倒退。

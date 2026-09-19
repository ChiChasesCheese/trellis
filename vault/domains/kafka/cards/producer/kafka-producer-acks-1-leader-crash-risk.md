---
id: kafka-producer-acks-1-leader-crash-risk
node: producer.acks-durability
type: qa
step: 3
source: kafka-2e
---
## Q
生产者把 `acks` 设置为 1 时，消息在什么条件下算「写入成功」？这个设置下消息还有可能丢失吗？

## A
`acks=1` 时，只要分区的首领副本（leader replica）收到消息，broker 就会告诉生产者写入成功，不需要等待跟随者副本（follower replica）完成复制。这比 acks=0 更安全，因为首领没收到消息时生产者会收到错误并重试；但如果首领刚确认收到消息就立刻崩溃，而消息还没来得及被复制到任何跟随者，新选出的首领就不会有这条消息，此时消息依然会丢失。

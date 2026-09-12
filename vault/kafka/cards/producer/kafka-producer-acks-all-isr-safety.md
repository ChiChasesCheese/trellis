---
id: kafka-producer-acks-all-isr-safety
node: producer.acks-durability
type: qa
source: kafka-2e
---
## Q
生产者把 `acks` 设置为 all，一条消息在什么条件下才会被判定为「写入成功」？为什么这比 acks=1 更能防止丢消息？

## A
acks=all 要求分区的所有同步副本（ISR，in-sync replicas，与首领保持同步的副本集合）都确认收到消息之后，生产者才会收到写入成功的响应。这样即使首领随后崩溃，新选出的首领也一定是 ISR 里已经拥有这条消息的某个副本，不会丢失数据；而 acks=1 只要求首领收到，一旦首领确认后立刻崩溃且消息还没复制给任何跟随者，消息就会丢失。

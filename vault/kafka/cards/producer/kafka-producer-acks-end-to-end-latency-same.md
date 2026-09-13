---
id: kafka-producer-acks-end-to-end-latency-same
node: producer.acks-durability
type: qa
source: kafka-2e
---
## Q
既然 acks 的值越小生产者延迟越低，那么把 acks 调低是不是也能降低消息「从生成到消费者可以读到」的端到端延迟？

## A
不会。不管 acks 设置成 0、1 还是 all，端到端延迟（从消息产生到消费者可以读取它）是一样的，因为 Kafka 为了保证一致性，只允许消费者读取已经被写入所有同步副本的消息，这个限制与生产者的 acks 设置无关。所以如果关心的是端到端延迟而不是生产者自己发送时的等待时间，就没有必要为了追求低延迟而牺牲可靠性，可以直接选择最安全的 acks=all。

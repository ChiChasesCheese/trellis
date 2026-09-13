---
id: kafka-reliability-four-core-guarantees
node: reliability.guarantees
type: cloze
source: kafka-2e
---
Kafka 对可靠性做出的四条基本保证是：{{c1::分区内消息有序（同一个生产者写入同一分区，先写的消息偏移量更小，消费者按此顺序读取）}}；{{c2::消息只有被写入分区的全部同步副本（ISR，in-sync replicas）后才算「已提交」，不要求先落盘}}；{{c3::只要还有一个副本存活，已提交的消息就不会丢失}}；{{c4::消费者只能读取到已提交的消息}}。这四条是 Kafka 能力的边界，本身并不等于「系统整体可靠」，还需要围绕它们做进一步的配置权衡。

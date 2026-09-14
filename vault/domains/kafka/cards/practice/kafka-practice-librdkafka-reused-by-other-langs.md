---
id: kafka-practice-librdkafka-reused-by-other-langs
node: practice.other-clients
type: qa
source: kafka-2e
---
## Q
librdkafka 是用 C 语言实现的 Kafka 客户端库，被认为是性能最好的 Kafka 客户端实现之一。为什么 Confluent 支持的 Go 语言、Python 和 .Net 客户端都选择基于它做封装，而不是各自用原生语言重新实现一遍 Kafka 协议？

## A
librdkafka 已经用 C 语言把 Kafka 客户端协议实现到了很高的性能水平，其他语言想要达到同等的性能和协议正确性，与其在自己的语言里从零重新实现一遍完整的 Kafka 客户端协议（工作量大、还要独自跟进协议演进和修复各类边界问题），不如直接给这个已经过验证、性能优异的 C 库套一层本语言的绑定（binding）。这样各语言客户端可以共享同一份底层实现的性能优势和协议正确性，只需要维护一层相对薄的语言绑定代码。

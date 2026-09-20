---
id: kafka-practice-python-two-client-options
node: practice.other-clients
type: qa
step: 3
source: kafka-2e
---
## Q
在 Python 生态里，同样存在两种不同性质的 Kafka 客户端：Confluent 支持、基于 librdkafka 封装的 Python 客户端，和 kafka-python（原生 Python 实现，Apache 2.0 许可）。这组对比和 Go 生态里 librdkafka 封装客户端与 Sarama 的对比是同一种模式吗？

## A
是同一种模式：基于 librdkafka 的 Python 客户端本质上是给 C 语言实现的 librdkafka 库套一层 Python 绑定，运行时依赖这个底层 C 库；kafka-python 则是完全用 Python 原生实现的 Kafka 客户端，不依赖 librdkafka，采用 Apache 2.0 许可。也就是说，无论是 Go 还是 Python，Kafka 客户端生态里都同时存在「封装 librdkafka」和「本语言原生实现」这两类选择，这是一个在多个非 JVM 语言生态里反复出现的共同模式。

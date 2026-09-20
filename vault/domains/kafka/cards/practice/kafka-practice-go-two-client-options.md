---
id: kafka-practice-go-two-client-options
node: practice.other-clients
type: qa
step: 2
source: kafka-2e
---
## Q
在 Go 语言生态里，接入 Kafka 至少有两种不同性质的客户端库可选：一种是 Confluent 支持、基于 librdkafka 封装的 Go 客户端，另一种是 Sarama（Shopify 开发、MIT 许可）。这两者在实现方式上有什么本质区别？

## A
基于 librdkafka 封装的 Go 客户端底层调用的是 C 语言实现的 librdkafka 库，Go 代码只是一层绑定，运行时依赖这个 C 库；Sarama 则是完全用 Go 语言原生实现的 Kafka 客户端，不依赖任何外部 C 库，从协议层到应用层都是纯 Go 代码，并采用 MIT 许可发布。两者代表了「复用一个高性能 C 库、语言层只做绑定」和「用目标语言原生实现整个客户端」这两种不同的技术路线。

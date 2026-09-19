---
id: kafka-practice-strimzi-bridge-no-schema-registry
node: practice.kubernetes-strimzi
type: qa
step: 2
source: kafka-2e
---
## Q
Strimzi 提供的 Strimzi Kafka Bridge 是什么类型的组件？为什么它目前还不支持模式注册表（schema registry，用于管理和校验消息格式模式的组件）这项能力？

## A
Strimzi Kafka Bridge 是一个基于 Apache 2.0 许可发布的 REST 代理（REST proxy）实现，它把 Kafka 的生产和消费能力通过 HTTP 接口暴露出来，方便那些不方便直接使用原生 Kafka 客户端协议的场景接入。目前它还不支持模式注册表功能，原因是出于许可方面的考虑——常见的模式注册表实现（比如 Confluent 的模式注册表）采用的许可协议限制了它们在某些场景下被自由集成，Strimzi 作为一个坚持使用 Apache 2.0 等宽松许可的开源项目，暂时无法把这类受限许可的组件直接整合进自己的产品中。

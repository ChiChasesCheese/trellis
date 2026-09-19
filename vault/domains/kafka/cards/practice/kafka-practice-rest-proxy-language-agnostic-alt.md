---
id: kafka-practice-rest-proxy-language-agnostic-alt
node: practice.other-clients
type: qa
step: 4
source: kafka-2e
---
## Q
除了为某种编程语言选择一个原生的 Kafka 客户端库（或封装 librdkafka 的绑定），还有什么方式可以让缺乏成熟原生客户端支持的语言或环境接入 Kafka？这种方式的好处是什么？

## A
可以使用 REST 代理（REST proxy，比如 Confluent、Strimzi 或 Karapace 提供的实现），它把 Kafka 的生产和消费能力通过标准的 HTTP 接口暴露出来。这样一来，任何能发送 HTTP 请求的编程语言或工具都可以接入 Kafka，不需要这个语言生态里存在专门维护的原生 Kafka 客户端库或协议实现，因此能够覆盖比「逐语言维护原生客户端」更广泛的应用场景，尤其适合客户端语言小众、或者不想为它单独引入一个原生客户端依赖的场景。

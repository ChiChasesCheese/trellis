---
id: kafka-producer-interceptor-hooks
node: producer.extensibility
type: qa
source: kafka-2e
---
## Q
Kafka 生产者拦截器（ProducerInterceptor）提供的 `onSend` 和 `onAcknowledgement` 两个方法分别在什么时机被调用？为什么用拦截器而不是直接改业务代码更适合做监控埋点这类需求？

## A
`onSend` 在记录被发送、甚至在被序列化之前调用，可以读取甚至修改这条记录，但必须返回一个合法的 ProducerRecord；`onAcknowledgement` 在收到 Kafka 的确认响应时调用，可以读取响应信息（如是否出错）但不能修改它。拦截器的好处是可以在完全不修改业务代码的前提下，给公司里所有使用同一套生产者配置的应用程序统一加上监控、打标头或脱敏之类的行为，尤其适合无法访问或不想改动原始业务代码的场景。

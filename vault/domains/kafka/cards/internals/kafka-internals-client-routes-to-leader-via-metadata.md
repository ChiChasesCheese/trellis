---
id: kafka-internals-client-routes-to-leader-via-metadata
node: internals.request-handling
type: qa
step: 1
source: kafka-2e
---
## Q
Kafka 的生产请求和获取请求必须发给分区的首领副本（leader replica）所在的 broker，但客户端一开始并不知道哪个 broker 是首领，它是怎么找到正确目标的？如果目标选错了会怎样？

## A
客户端会先发送一种叫**元数据请求（metadata request）**的请求，可以发给集群里任意一个 broker（因为所有 broker 都缓存了完整的集群元数据），得到的响应里列出了每个主题各分区的副本分布和当前首领是谁。客户端把这些信息缓存下来，之后直接把生产/获取请求发给目标分区首领所在的 broker，并定期（由 `metadata.max.age.ms` 控制刷新间隔）刷新缓存。如果分区首领已经变化，客户端拿旧缓存发错了 broker，会收到「非分区首领」错误，客户端会先刷新元数据再重发请求。

---
id: kafka-admin-kafkafuture-nonblocking
node: admin.topic-ops
type: qa
source: kafka-2e
---
## Q
在一个需要持续处理大量客户端请求的服务器里，用 AdminClient 的 describeTopics 之类方法查询 Kafka 状态时，为什么直接对返回结果调用 Future.get() 可能是个问题？应该怎么做？

## A
get() 会阻塞当前线程，直到 Kafka 真正返回响应或超时；如果这次调用发生在服务器处理请求的线程里，就意味着这个线程要一直等 Kafka 响应完才能继续处理别的客户端请求，拖慢整个服务的吞吐量。更好的做法是使用 AdminClient 返回的 KafkaFuture 提供的非阻塞接口（如注册 whenComplete 回调），让服务器线程立即返回去处理别的请求，等 Kafka 真正返回结果或抛出异常时再异步执行回调，把结果发给对应的客户端；这样即使某一次查询等待很久，也不会拖慢其他请求的响应速度。

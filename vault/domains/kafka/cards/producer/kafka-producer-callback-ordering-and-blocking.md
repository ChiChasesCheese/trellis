---
id: kafka-producer-callback-ordering-and-blocking
node: producer.client-basics
type: qa
source: kafka-2e
---
## Q
使用异步发送并传入回调（callback）时，如果连续向同一个分区发送了两条消息，它们的回调会按什么顺序执行？回调函数里能不能做耗时的阻塞操作？

## A
回调在生产者的主线程里执行，如果两条消息被发往同一个分区，它们的回调会按照发送的先后顺序被依次调用。正因为回调运行在这条关键线程上，回调本身必须执行得快，不应该包含阻塞操作（比如同步 I/O）——否则会拖慢生产者处理后续消息的速度，阻塞操作应该被放到其他线程去做。

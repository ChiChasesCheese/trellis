---
id: kafka-consumer-graceful-shutdown-wakeup
node: consumer.client-basics
type: qa
step: 5
source: kafka-2e
---
## Q
消费者的轮询循环通常写成一个无限循环，要怎样才能从另一个线程安全地让它优雅退出？为什么不能直接从其他线程调用 `poll()` 之外的方法？

## A
应该在另一个线程（比如关闭钩子 ShutdownHook）里调用 `consumer.wakeup()`——这是消费者唯一一个可以从其他线程安全调用的方法。调用它会让正在阻塞的（或者下一次调用的）`poll()` 抛出 `WakeupException`，主线程捕获这个异常后跳出循环，并调用 `consumer.close()`；关闭时消费者会自动提交尚未提交的偏移量，并通知协调器自己正在离开群组，从而立即触发再均衡，不需要等待会话超时。

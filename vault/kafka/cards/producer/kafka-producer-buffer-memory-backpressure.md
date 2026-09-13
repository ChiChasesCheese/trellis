---
id: kafka-producer-buffer-memory-backpressure
node: producer.batching-throughput
type: qa
source: kafka-2e
---
## Q
如果应用程序调用 `send()` 的速度超过了生产者把消息发给 broker 的速度，生产者内部的发送缓冲区（由 `buffer.memory` 控制大小）会发生什么？

## A
生产者的内存缓冲区可能会被耗尽，此时后续的 `send()` 调用会被阻塞，等待有内存被释放出来；如果等待时间超过了 `max.block.ms`，就会抛出异常。需要注意，这个异常是从 `send()` 方法本身直接抛出的，而不是像发送失败那样通过返回的 Future 对象抛出。

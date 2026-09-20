---
id: kafka-consumer-poll-liveness-requirement
node: consumer.client-basics
type: qa
step: 4
source: kafka-2e
---
## Q
为什么消费者必须持续、频繁地调用 `poll()`，而不能只在有需要处理消息时才偶尔调一次？如果太久没调用会发生什么？

## A
`poll()` 不仅仅是拉取数据的接口，消费者靠不断调用它来向群组证明自己还「活跃」；如果超过 `max.poll.interval.ms` 没有调用 `poll()`，群组协调器会认为这个消费者已经「死亡」，把它负责的分区转移给群组里的其他消费者（触发再均衡）。所以轮询循环里不能有可能长时间阻塞的操作，否则即使消费者进程本身还在运行，也会被错误地判定为失效而被踢出群组。

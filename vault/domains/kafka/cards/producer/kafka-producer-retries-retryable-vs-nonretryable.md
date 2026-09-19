---
id: kafka-producer-retries-retryable-vs-nonretryable
node: producer.timeouts-retries
type: qa
step: 3
source: kafka-2e
---
## Q
生产者收到 broker 返回的错误后，是不是所有错误都会触发自动重试？

## A
不是。Kafka 会区分可重试错误和不可重试错误：像「非分区首领」这类暂时性错误（例如首领正在重新选举），只要重试通常就能解决，生产者会按 `retries` 参数自动重试，重试间隔由 `retry.backoff.ms` 控制；而「消息太大」这类本质性错误不会因为重试而改变结果，生产者不会重试，会立即把异常抛给应用。因此应用只需集中处理不可重试错误或重试次数耗尽的情况，可重试错误不需要自己实现重试逻辑。

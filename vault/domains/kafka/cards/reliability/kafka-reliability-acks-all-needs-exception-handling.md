---
id: kafka-reliability-acks-all-needs-exception-handling
node: reliability.producer-reliable
type: qa
step: 4
source: kafka-2e
---
## Q
把 `acks` 设为 `all` 之后，是不是就自动保证生产者不会丢消息了？一个典型的反例是什么？

## A
不是。`acks=all` 只保证「如果消息被确认成功，那么它一定已经写入所有同步副本」，但它不负责处理「消息还没被确认成功」时发生的异常。一个典型的反例：生产者发消息时分区首领刚好崩溃、新首领还在选举中，broker 会向生产者返回「首领不可用」这类错误响应；如果生产者的代码没有正确捕获这个异常并重试，消息就直接丢了。这不是 broker 可靠性问题（broker 根本没收到消息），也不是一致性问题（消费者也读不到它），纯粹是因为应用代码没有妥善处理这个报错——说明「配置对 acks」和「代码里正确处理异常/重试」缺一不可。

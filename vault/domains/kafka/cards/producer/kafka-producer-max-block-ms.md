---
id: kafka-producer-max-block-ms
node: producer.timeouts-retries
type: qa
step: 2
source: kafka-2e
---
## Q
`max.block.ms` 控制的是生产者哪个阶段的阻塞？和 `delivery.timeout.ms` 有什么区别？

## A
`max.block.ms` 控制的是调用 `send()`（或调用 `partitionsFor()` 查询元数据）时，生产者因为发送缓冲区已满或元数据不可用而发生阻塞的最长时间，超时会抛出超时异常，这发生在消息还没被真正放入批次、开始走发送流程之前。而 `delivery.timeout.ms` 是消息已经进入批次之后、到最终确认成功或彻底失败之间的时间预算，两者对应发送过程中前后不同的阶段。

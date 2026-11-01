---
id: hi-sd-kafka-7-retries
node: qb.sd.job-scheduler-cron-history.pre-sd-deep-dives-kafka
type: qa
step: 7
---
## Q
**生产者重试、消费者重试与死信队列**｜系统设计 · 深入技术

消息进出 Kafka 失败时怎么处理？Kafka 自带消费者重试吗？

## A
**生产者。** 网络或 broker 暂时故障时，生产者支持自动重试。开启重试必须同时开启幂等生产者（idempotent producer），避免「误以为没发出去」而重复写入。

**消费者。** Kafka 不提供开箱即用的消费者重试，要自己实现：把失败消息转到专门的重试 topic，由另一个消费者处理，不影响主消费者；重试次数过多就送入死信队列（DLQ）保存，供之后排查。

**取舍。** 爬虫题里选 SQS 而不是 Kafka，正是因为 SQS 内置重试与 DLQ，不必自己实现。

**数字。** 至少一次是默认语义；恰好一次需要幂等生产者加事务 API 等额外配置。

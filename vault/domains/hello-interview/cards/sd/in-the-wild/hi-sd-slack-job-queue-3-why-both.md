---
id: hi-sd-slack-job-queue-3-why-both
node: sd.in-the-wild.slack-job-queue.exam
type: qa
step: 3
---
## Q
**为什么是 Kafka 放在前面，而不是替换 Redis**｜系统设计 · 业界案例

既然 Redis 撑不住积压，为什么 Slack 没有把队列整个改建在 Kafka 上，或者换成 RabbitMQ、SQS？

## A
**要点。** 他们选了最小可行改动：Web 应用把任务写入 Kafka，Kafka 持久缓冲一切；中继服务按受控速率把任务从 Kafka 排入 Redis；Redis 仍只保留一个短队列，并提供应用已熟悉的语义。入队接口和 worker 一侧都不变。

**为什么。** Kafka 是落盘的追加日志，受保留时间而非内存限制，突发只会让日志变长。但偏移量（offset）只是分区里的位置，不是单个任务的状态，逐任务确认、重试、去重、在途跟踪都要自己在上面构建（重试做成重新入队，去重用小型键值存储）。这些语义 Slack 早已在 Redis 中实现，多年的应用代码依赖其精确行为，全部改写会把一次范围明确的可用性修复变成重写。

**对照。** RabbitMQ、SQS、beanstalkd 都能落盘，但各有自己的投递语义，换哪个都是对着另一套 API 重写。只留 Redis 就是刚刚失败的设计。

**取舍。** 两个类似队列的系统增加了运维，换来的是风险小、可分步推进。

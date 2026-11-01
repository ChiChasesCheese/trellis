---
id: hi-sd-web-crawler-4-fetch-retry
node: sd.problem-breakdowns.web-crawler
type: qa
step: 4
---
## Q
**拉取失败的重试与崩溃恢复**｜系统设计 · 问题拆解

爬虫拉取网页经常失败。重试（带指数退避）有哪三种做法？爬虫宕机后，正在处理的 URL 怎样不丢？

## A
**取舍。**
- 差：内存计时器等几秒再试。机器一挂计时器就丢了，而且几秒后多半还没恢复。
- 可行：Kafka 另开失败主题，把「下次重试时间」写进消息，由单独服务读取并等待。能用，但要自己实现和维护。
- 最佳：SQS。消息被收下但未删除，可见性超时（visibility timeout）到期后会重新可见。每次失败后按 ApproximateReceiveCount 算出新的超时并调用 ChangeMessageVisibility，实现指数退避；超过 maxReceiveCount（假设 5 次）自动进死信队列（DLQ），视为站点下线。

**崩溃恢复。** 爬虫只在 HTML 成功入库后才确认。Kafka 靠偏移量（offset）：成功前不提交，换一个消费者接着读。SQS 靠可见性超时：没删除的消息自动回到队列，成功后才删除。解析 worker 同理。

**易错。** 选型没有标准答案，说清取舍就行；不熟悉细节时，这里可以不深入。

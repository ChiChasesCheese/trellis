---
id: hi-c-sd-web-crawler-n07-retry
node: sd.problem-breakdowns.web-crawler.notes
type: qa
step: 7
---
## Q
**网络爬虫 · 深入一：拉取失败怎样重试**｜摘要 · 必会

拉取 URL 失败时，内存计时器、Kafka 手写退避、SQS 退避三种做法各有什么问题？指数退避怎么实现？

## A
- **差：内存计时器。** 等几秒再试。爬虫宕机，计时器就丢了；而且站点几秒后多半还没恢复，需要指数退避（exponential backoff，每次失败后等待时间翻倍）。
- **可以：Kafka 加手写退避。** Kafka 本身不支持重试，要另开失败主题，由单独服务读取，把"下次重试时间"写进消息，消费者发现时间还没到就等。能用，但实现和维护都复杂。
- **最好：SQS。** SQS 没有现成的退避开关，但有可见性超时（visibility timeout）：消息被收下却没删除，超时后会重新可见（默认 30 秒，最长 12 小时）。失败后根据 `ApproximateReceiveCount`（已被收到的次数）算出新超时，调用 `ChangeMessageVisibility` 设置，消息就被藏到该重试的时候。
- **终止：** 不能无限重试；队列的 redrive 策略设 `maxReceiveCount`，超过后自动进死信队列（DLQ），这里取 5 次后视为站点下线。
- **选型态度：** 没有绝对对错，能说清取舍即可；不熟悉细节时，这里不必深挖。

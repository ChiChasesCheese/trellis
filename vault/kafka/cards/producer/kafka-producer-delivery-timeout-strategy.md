---
id: kafka-producer-delivery-timeout-strategy
node: producer.timeouts-retries
type: qa
source: kafka-2e
---
## Q
应该如何配置 `delivery.timeout.ms`，才能既保证「broker 崩溃、首领重新选举期间还能继续重试」，又不用手动精确纠结 `retries` 该设多大？

## A
建议把 `delivery.timeout.ms` 直接设置成你愿意让生产者持续重试的最长时间（例如已知首领选举通常需要约30秒，出于保险设置为120秒），同时保留默认的、几乎无限制的 `retries` 次数。这样生产者只要还在 `delivery.timeout.ms` 规定的时间窗口内，就会一直重试，不需要再单独精确计算重试次数和重试间隔的组合。

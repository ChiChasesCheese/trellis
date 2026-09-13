---
id: kafka-consumer-session-timeout-heartbeat-interval-ratio
node: consumer.poll-config
type: qa
source: kafka-2e
---
## Q
`session.timeout.ms`（消费者可以多久不发心跳仍被认为存活，默认10秒）和 `heartbeat.interval.ms`（消费者发送心跳的频率）之间通常应该保持什么比例关系？把 `session.timeout.ms` 调小或调大分别有什么后果？

## A
通常把 `heartbeat.interval.ms` 设置为 `session.timeout.ms` 的三分之一左右（例如会话超时3秒、心跳间隔1秒），这样在真正超时之前至少能有几次心跳发送机会，避免网络抖动导致误判。把 `session.timeout.ms` 设置得比默认值小，可以更快检测到消费者崩溃并把它的分区转移出去，但也更容易因为短暂的网络延迟等原因触发不必要的再均衡；设置得比默认值大则相反，误判变少但发现真实故障要花更久时间。

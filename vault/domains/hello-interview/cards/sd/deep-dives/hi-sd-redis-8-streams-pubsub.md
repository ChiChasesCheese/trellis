---
id: hi-sd-redis-8-streams-pubsub
node: qb.sd.messenger-chat-system.pre-sd-deep-dives-redis
type: qa
step: 8
---
## Q
**Redis 流与发布订阅**｜系统设计 · 深入技术

Redis Streams 与 Pub/Sub 有什么区别？什么时候该用 Kafka？为什么不要自己用键存订阅者地址来实现 Pub/Sub？

## A
**要点。** Streams 是追加日志，用 `XADD` 写入，消费者组（`XREADGROUP`）协调谁处理哪条。worker 读取、处理、确认；消费者死亡后，条目的空闲时间不断增长，另一个 worker 用 `XCLAIM` 或 `XAUTOCLAIM` 接手。由于分不清慢和死，同一条可能被处理两次，所以处理要幂等；持久程度也取决于持久化设置。

Pub/Sub 只投递给此刻在线的订阅者，消息不持久，至多一次；订阅者离线就错过。Redis 7 之后有分片 Pub/Sub（`SPUBLISH`、`SSUBSCRIBE`），频道按槽路由，容量随集群扩展，不再是每条消息广播到所有节点。连接开销按节点算，不是按频道。

**取舍。** 队列规模不大且已经有 Redis（后台任务、通知扇出）用 Streams；需要长期保留、多个独立消费者重放、不能丢消息的高吞吐时用 Kafka。需要离线投递，可配合队列或发件箱（outbox）。

**易错。** 自己用「主题键对应订阅者服务器地址集合」实现，要三跳（查键、返回、逐个发送），后一跳还要新建连接，并且要用心跳或 TTL 清理宕机服务器。看起来像 Pub/Sub 就直接用 Pub/Sub。

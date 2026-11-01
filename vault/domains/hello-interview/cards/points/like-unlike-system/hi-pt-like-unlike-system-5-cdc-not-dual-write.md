---
id: hi-pt-like-unlike-system-5-cdc-not-dual-write
node: qb.sd.like-unlike-system.points
type: qa
step: 5
---
## Q
**点赞与取消点赞系统 · 用变更流代替双写**｜出自：点赞与取消点赞系统 › 整体设计

点赞系统写完事实表后需要发计数事件。为什么不在服务里写库再发消息？

## A
**问题。** 双写可能一个成功一个失败，计数就漂移。
**做法。** 让数据库变更流（CDC，如 DynamoDB Streams、binlog）驱动 Kafka，保证记录变了就一定有事件；事件按 itemId 分区。
**取舍。** 增量事件至少一次投递，需事件 ID 去重。

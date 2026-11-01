---
id: hi-pt-twitter-clone-feed-8-shard-fanout-reliability
node: qb.lld.twitter-clone-feed.points
type: qa
step: 8
---
## Q
**微博客与个性化信息流 · 分片与扇出可靠性**｜出自：微博客与个性化信息流 › 深入 3

推文库、关注关系怎么分片？扇出 Worker 如何保证可靠，失败重试为什么安全？

## A
**分片。** 推文库按推文 ID 分片；个人页另有按 `(authorId, 时间)` 的索引。关注正向表按 followerId 分片，反向表按 followeeId 分片；大 V 粉丝列表分页读，扇出任务按分片并行。
**可靠性。** Worker 水平扩展，Kafka 按作者 ID 分区；一次扇出分成每批几千个粉丝，失败批重试。写入幂等：有序集合里同一个 ID 只有一份。
**延迟。** 活跃粉丝优先投递，其余延后。

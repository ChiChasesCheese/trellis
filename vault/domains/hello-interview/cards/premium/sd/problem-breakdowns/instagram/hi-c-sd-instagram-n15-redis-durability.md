---
id: hi-c-sd-instagram-n15-redis-durability
node: sd.problem-breakdowns.instagram.notes
type: qa
step: 15
---
## Q
**Instagram 图片分享 · Redis 动态流的高可用与持久化**｜摘要 · 追问

用 Redis 存预计算的动态流，面试官问"实例挂了怎么办"，要答哪些点？

## A
- **风险：** 没配持久化，Redis 重启或宕机后所有动态流数据丢失，大量用户的流变空、服务降级。
- **高可用：** Redis Sentinel 监控主从，主挂了自动选新主（failover）。
- **容量与分片：** 用 Redis Cluster 把数据分片到多个节点，单节点放不下的总量也能容纳。
- **持久化：** AOF（追加日志）或 RDB（定时快照）二选一或组合，恢复时丢得少。
- **一句话版本：** "Redis 开 AOF 持久化，用 Sentinel 做故障转移，节点故障只丢很少数据"，说明你没把 Redis 当黑盒。

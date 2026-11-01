---
id: hi-sd-distributed-rate-limiter-7-scale-shard
node: sd.problem-breakdowns.distributed-rate-limiter
type: qa
step: 7
---
## Q
**扩展到每秒 100 万请求：分片 Redis**｜系统设计 · 问题拆解

单个 Redis 为什么撑不住 100 万请求每秒？怎么分片，分片键是什么？生产里通常怎么做？

## A
**数字。** 单个 Redis 约 10 到 20 万次操作 / 秒；一次限流检查至少包含读（HMGET）与写（HSET），因此只能支撑约 5 到 10 万次检查 / 秒。目标 100 万 / 秒，需要约 10 个分片，每个约 10 万。

**分片规则。** 同一客户端的所有请求必须落到同一个分片，否则状态被拆开就没用了。用一致性哈希：登录用户哈希用户 ID，匿名用户哈希 IP，API 请求哈希 API key。令牌桶算法本身不变，只是网关带着路由逻辑去找对应的 Redis。

**生产做法。** 用 Redis Cluster：把键分到 16384 个哈希槽，再分配给多个节点，`alice:bucket` 的路由由集群自动处理，不用在网关里自己写一致性哈希。

**模式。** 这是写扩展（Scaling Writes）：每秒百万次原子读改写。

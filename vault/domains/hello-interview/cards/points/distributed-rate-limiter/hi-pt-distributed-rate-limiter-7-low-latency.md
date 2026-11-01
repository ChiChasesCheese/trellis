---
id: hi-pt-distributed-rate-limiter-7-low-latency
node: qb.sd.distributed-rate-limiter.points
type: qa
step: 7
---
## Q
**分布式限流器 · 降低检查延迟**｜出自：分布式限流器 › 深入 4

分布式限流器每次检查都要访问 Redis，怎样把延迟压下来？有哪些进阶方案，代价是什么？

## A
**基础。** 网关与 Redis 保持长连接池避免握手，就近部署同一区域；跨区域各自限流，接受最终一致。
**进阶。** 网关一次从 Redis 领一批令牌在本地发放，Redis 压力降一个数量级。
**代价。** 限额变近似，一个网关最多多放行一批，重启会丢未用完的令牌。
**顺序。** 先做连接池和就近部署，批领留作追问。

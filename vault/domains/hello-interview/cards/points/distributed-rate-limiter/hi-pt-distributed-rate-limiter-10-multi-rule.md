---
id: hi-pt-distributed-rate-limiter-10-multi-rule
node: qb.sd.distributed-rate-limiter.points
type: qa
step: 10
---
## Q
**分布式限流器 · 多规则与同分片**｜出自：分布式限流器 › 取舍与追问

分布式限流器要同时满足"每秒 10 次且每天 1 万次"两条规则。怎么实现，要注意什么？

## A
**要点。** 每条规则各自一个键，一次请求在脚本里检查多个键，全部通过才扣减。
**易错。** 这些键必须落在同一分片（用 hash tag `{clientId}`），否则要多次往返，也无法原子。
**客户端体验。** 超限返回 429 加 Retry-After，让客户端指数退避，避免重试风暴。

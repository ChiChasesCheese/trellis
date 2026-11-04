---
id: hi-sd-distributed-rate-limiter-9-latency
node: sd.problem-breakdowns.distributed-rate-limiter.exam
type: qa
step: 9
---
## Q
**降低限流检查的延迟**｜系统设计 · 问题拆解

每次限流检查要访问 Redis，如何控制延迟？哪些优化值得在面试里提，哪些不必？

## A
**最重要：连接池。** 网关保持到 Redis 的持久连接池，省掉每次 TCP 握手（可能 20 到 50ms），按请求量与 Redis 响应时间调池大小。

**收益最大：地理分布。** 在多个地区部署网关和 Redis 集群，东京用户访问弗吉尼亚的 Redis 会慢很多。代价是跨地区数据一致性，但限流可以接受地区间最终一致，换取低延迟。

**简要提及即可。**
- 本地缓存限流状态：陈旧数据会导致错误决策，有风险
- **pipelining 减少往返：** Redis pipelining 或 Lua 批量操作，减少往返
- 请求批处理

**取舍。** 这些优化增加复杂度，连接池和地理分布做好后通常没必要，除非面试官追问，否则不主动提。

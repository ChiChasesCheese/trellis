---
id: hi-sd-networking-essentials-8-failure-handling
node: qb.sd.messenger-chat-system.pre-sd-core-concepts-networking-essentials
type: qa
step: 8
---
## Q
**超时重试与熔断**｜系统设计 · 核心概念

调用下游失败是常态。面试里怎样回答重试（retry）、退避（backoff）、幂等（idempotency）和熔断（circuit breaker）？

## A
**要点。**
- 超时加重试：处理瞬时故障，前提是接口幂等。
- 指数退避加抖动（jitter）：每次重试等待翻倍，再加随机量，否则所有客户端同步重试，像锤子一样反复砸向恢复中的服务。面试官想听到「retry with exponential backoff」，资深岗位会追问抖动。
- 幂等键（idempotency key）：写操作带唯一键，服务端检查是否处理过或正在处理，只执行一次。例如扣款不能因重试扣两次。
- 熔断：监控失败率，超过阈值就打开，直接快速失败；一段时间后进入半开，放少量探测请求，成功则关闭、失败则继续打开。

**为什么。** 数据库宕机后，无节制的重试和用户涌入会让它起不来（惊群，thundering herd）。熔断能快速失败、给下游喘息、避免级联故障。

**使用时机。** 被追问「某服务挂了会怎样」时，用于外部 API、数据库连接、微服务调用。

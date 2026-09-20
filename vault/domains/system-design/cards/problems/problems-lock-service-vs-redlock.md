---
id: problems-lock-service-vs-redlock
node: problems.foundations.lock-service
type: qa
step: 4
tags: [grown]
---
## Q
In a distributed lock service design, why is a Redlock-style scheme (acquiring a TTL'd key on a majority of independent Redis instances) not an acceptable foundation when lock correctness is a safety dependency, as opposed to a pure efficiency optimization?

## A
Redlock's safety depends on a set of timing assumptions — bounded process pauses, bounded network delay, bounded clock drift — that don't hold in real systems (a long GC pause alone can violate them). More fundamentally, its protocol structurally cannot produce a verifiable, monotonically increasing fencing token, because there is no shared, agreed-upon logical clock across the independent Redis instances the way a consensus-replicated log's commit position provides one. This makes it acceptable for uses where a failed lock only costs some duplicated work (pure efficiency), but not for uses where a downstream resource needs to reject a stale writer's request, since there is no token to check against.

## Q zh
在一个分布式锁服务设计中，当锁的正确性是一项安全性依赖、而不是纯粹的效率优化时，为什么 Redlock 式的方案（在多个独立 Redis 实例的多数上都获取一个带 TTL 的 key）不是一个可以接受的地基？

## A zh
Redlock 的安全性依赖一组时序假设——进程暂停有界、网络延迟有界、时钟漂移有界——这些假设在真实系统里并不成立（单是一次较长的 GC 暂停就可能违反它们）。更根本的是，它的协议在结构上根本产生不出一个可验证的单调递增 fencing token，因为这些相互独立的 Redis 实例之间没有像共识复制日志的提交位置那样，一个所有人都认可的共享逻辑时钟。这使得它在锁失败只会造成一些重复劳动（纯效率优化）的场景里可以接受，但在下游资源需要拒绝一个过期写入者的请求、却没有令牌可以校验的场景里不可接受。

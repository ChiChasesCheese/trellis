---
id: problems-job-scheduler-multi-tenant-weighted-fairness
node: problems.foundations.job-scheduler
type: qa
step: 8
tags: [grown]
---
## Q
In a distributed job scheduler shared by thousands of tenants, why does plain FIFO dispatch fail the requirement that one tenant's job burst must not systematically delay other tenants, and what mechanism fixes it without resorting to full per-tenant infrastructure isolation?

## A
Under FIFO dispatch, any tenant's traffic spike is served strictly in arrival order alongside everyone else's jobs, so a burst from one tenant directly translates into delayed on-time triggering for every other tenant sharing the same dispatch path and worker pool -- there is no mechanism separating 'this tenant is over its normal share' from 'this tenant is dispatching normally.' The fix is a per-tenant token-bucket rate limiter combined with dynamic priority: tenants that persistently exceed their allotted share get their subsequent jobs marked lower priority, and the dispatch queue processes different priority levels via weighted round-robin, so high-priority (normal-rate) tenants get served more often while low-priority (bursting) tenants still make progress without being starved -- confining one tenant's burst to mostly affecting its own latency instead of everyone else's.

## Q zh
在一个被数千个租户共享的分布式任务调度器里，为什么普通的 FIFO 分发满足不了「一个租户的任务洪峰不能系统性拖慢其他租户」这条要求？在不采用完全按租户做基础设施硬隔离的前提下，什么机制能修复这个问题？

## A zh
在 FIFO 分发下，任何租户的流量突增都严格按到达顺序和其他所有租户的任务混在一起处理，所以一个租户的突发流量会直接转化为共享同一分发路径和 worker 池的其他所有租户触发延迟——没有任何机制能区分「这个租户超出了它正常的份额」和「这个租户在正常分发」。修复办法是按租户维护令牌桶（token bucket）速率限制器，配合动态优先级：持续超出自己配额的租户，后续任务会被标记为低优先级，分发队列按加权轮询（weighted round-robin）处理不同优先级，让高优先级（正常速率）的租户被更频繁地服务，同时低优先级（突发中）的租户依然能推进、不会被饿死——把一个租户洪峰的影响限制在主要拖慢它自己，而不是所有人。
